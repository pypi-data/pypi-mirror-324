import os
from pathlib import Path


def generate_tree(nodes, base_path, dry_run=False, force=False):
    """
    Recursively generate files and directories from a list of Node objects.
    :param nodes: List of Node objects (from parser.py)
    :param base_path: pathlib.Path object where the tree should be created.
    :param dry_run: If True, only print what would be created.
    :param force: If True, overwrite existing files.
    """
    for node in nodes:
        # Clean the name by stripping any trailing slash for directories.
        name = node.name.rstrip("/") if node.is_dir else node.name
        target = base_path / name

        if node.is_dir:
            if dry_run:
                print(f"[DRY RUN] Would create directory: {target}")
            else:
                if not target.exists():
                    try:
                        target.mkdir(parents=True, exist_ok=True)
                        print(f"Created directory: {target}")
                    except Exception as e:
                        raise Exception(f"Could not create directory {target}: {e}")
                elif force:
                    print(f"Directory already exists and --force was used: {target}")
            if node.children:
                generate_tree(node.children, target, dry_run=dry_run, force=force)
        else:
            if dry_run:
                print(f"[DRY RUN] Would create file: {target}")
            else:
                if target.exists() and not force:
                    print(f"File already exists (skipped): {target}")
                else:
                    try:
                        # Ensure the parent directory exists.
                        target.parent.mkdir(parents=True, exist_ok=True)
                        with open(target, "w") as f:
                            # Create an empty file.
                            pass
                        print(f"Created file: {target}")
                    except Exception as e:
                        raise Exception(f"Could not create file {target}: {e}")
