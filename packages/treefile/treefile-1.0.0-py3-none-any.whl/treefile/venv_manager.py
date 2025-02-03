import sys
import subprocess
import venv
from pathlib import Path


def create_virtualenv(base_path, venv_name, python_version, dry_run=False):
    """
    Create a virtual environment in the specified base_path with the given name.
    If python_version is different from the current interpreter, attempt to call that interpreter.
    :return: Path to the created virtual environment.
    """
    venv_path = Path(base_path) / venv_name
    if dry_run:
        print(f"[DRY RUN] Would create virtual environment at {venv_path} using interpreter: {python_version}")
        return venv_path

    if venv_path.exists():
        print(f"Virtual environment already exists at {venv_path}")
    else:
        if python_version != sys.executable:
            # Attempt to create the venv using the specified python version.
            cmd = [python_version, "-m", "venv", str(venv_path)]
            try:
                subprocess.check_call(cmd)
                print(f"Created virtual environment using {python_version} at {venv_path}")
            except Exception as e:
                raise Exception(f"Failed to create virtual environment using {python_version}: {e}")
        else:
            try:
                builder = venv.EnvBuilder(with_pip=True)
                builder.create(str(venv_path))
                print(f"Created virtual environment at {venv_path}")
            except Exception as e:
                raise Exception(f"Failed to create virtual environment: {e}")
    return venv_path


def activate_virtualenv(venv_path):
    """
    Activate the virtual environment.
    Because a subprocess cannot modify its parent’s shell, this function spawns a new shell with the venv activated.
    """
    import platform

    venv_path = Path(venv_path)
    system = platform.system()
    if system == "Windows":
        activate_script = venv_path / "Scripts" / "activate.bat"
        if not activate_script.exists():
            raise FileNotFoundError(f"Activation script not found at {activate_script}")
        print("Launching a new command prompt with the virtual environment activated...")
        subprocess.call(["cmd.exe", "/K", str(activate_script)])
    else:
        activate_script = venv_path / "bin" / "activate"
        if not activate_script.exists():
            raise FileNotFoundError(f"Activation script not found at {activate_script}")
        print("Launching a new shell with the virtual environment activated...")
        subprocess.call(["bash", "--rcfile", str(activate_script)])
