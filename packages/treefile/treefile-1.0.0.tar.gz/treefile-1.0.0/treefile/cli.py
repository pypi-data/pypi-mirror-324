import sys
import subprocess
import click
import yaml
from pathlib import Path
from .parser import parse_treefile
from .core import generate_tree
from .venv_manager import create_virtualenv, activate_virtualenv
from .utils import should_reprocess

DEFAULT_CONFIG_FILE = Path(__file__).parent.parent / "config.yaml"

def load_config():
    if DEFAULT_CONFIG_FILE.exists():
        with open(DEFAULT_CONFIG_FILE, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)
    return {}

@click.command()
@click.option("--file", "treefile_path", required=True, type=click.Path(exists=True), help="Path to the .treefile file")
@click.option("--output", type=click.Path(), default=".", help="Output directory (default: current directory)")
@click.option("--venv", "venv_name", default=None, help="Name for virtual environment (default: from config or .venv)")
@click.option("--py", "python_version", default=None, help="Python version for virtual environment (default: global python)")
@click.option("--activate", is_flag=True, default=False, help="Activate virtual environment upon completion")
@click.option("--dry-run", is_flag=True, default=False, help="Preview the file tree without creating files or directories")
@click.option("--force", is_flag=True, default=False, help="Overwrite existing files/directories if conflicts occur")
@click.option("--version", is_flag=True, default=False, help="Show package version")
def main(treefile_path, output, venv_name, python_version, activate, dry_run, force, version):
    """Generate a file tree based on a .treefile configuration."""
    from . import __version__

    if version:
        click.echo(f"treefile version {__version__}")
        sys.exit(0)

    config = load_config()
    if venv_name is None:
        venv_name = config.get("venv", ".venv")
    if python_version is None:
        python_version = config.get("python", sys.executable)
    if output == ".":
        output = config.get("output", ".")

    treefile_abs = Path(treefile_path).resolve()
    if not force and not dry_run and treefile_abs.exists():
        if not should_reprocess(treefile_abs):
            click.echo("No changes detected in the .treefile file. Skipping generation.")
            sys.exit(0)

    with open(treefile_abs, "r", encoding="utf-8") as f:
        lines = f.readlines()

    # Process embedded options if present.
    embedded_options = {}
    if lines:
        first_line = lines[0].strip()
        if first_line.startswith("#!treefile:"):
            parts = first_line[len("#!treefile:"):].strip().split()
            i = 0
            while i < len(parts):
                opt = parts[i]
                if opt.startswith("--"):
                    if i + 1 < len(parts) and not parts[i + 1].startswith("--"):
                        embedded_options[opt.lstrip("-")] = parts[i + 1]
                        i += 2
                    else:
                        embedded_options[opt.lstrip("-")] = True
                        i += 1
                else:
                    i += 1
            lines = lines[1:]

    if venv_name is None and "venv" in embedded_options:
        venv_name = embedded_options["venv"]
    if python_version is None and "py" in embedded_options:
        python_version = embedded_options["py"]
    if not activate and "activate" in embedded_options:
        activate = embedded_options["activate"] is True or str(embedded_options["activate"]).lower() in ("true", "1")

    treefile_content = "".join(lines)
    try:
        tree_nodes = parse_treefile(treefile_content)
    except Exception as e:
        click.echo(f"Error parsing the .treefile file: {e}", err=True)
        sys.exit(1)

    base_path = Path(output).resolve()
    if not base_path.exists():
        try:
            base_path.mkdir(parents=True)
        except Exception as e:
            click.echo(f"Error creating output directory {base_path}: {e}", err=True)
            sys.exit(1)

    try:
        generate_tree(tree_nodes, base_path, dry_run=dry_run, force=force)
    except Exception as e:
        click.echo(f"Error generating file tree: {e}", err=True)
        sys.exit(1)

    if venv_name:
        try:
            # If exactly one top-level node is a directory, use that as the project root.
            if len(tree_nodes) == 1 and tree_nodes[0].is_dir:
                project_root = base_path / tree_nodes[0].name.rstrip("/")
            else:
                project_root = base_path
            venv_path = create_virtualenv(project_root, venv_name, python_version, dry_run=dry_run)
        except Exception as e:
            click.echo(f"Error creating virtual environment: {e}", err=True)
            sys.exit(1)
        if activate:
            try:
                activate_virtualenv(venv_path)
            except Exception as e:
                click.echo(f"Error activating virtual environment: {e}", err=True)
                sys.exit(1)

    click.echo("File tree generation complete.")

if __name__ == "__main__":
    main()
