import platform
import os
from pathlib import Path

def get_icon_path(os_name):
    """
    Determine the appropriate icon file based on the operating system.
    The icon files are stored in the treefile/icons folder.
    """
    base_dir = Path(__file__).parent / "icons"
    if os_name == "Windows":
        icon_file = base_dir / "treefile.ico"
    elif os_name == "Darwin":
        icon_file = base_dir / "treefile.icns"
    else:
        icon_file = base_dir / "treefile.png"
    return str(icon_file.resolve())

def register_context_menu():
    system = platform.system()
    if system == "Windows":
        register_context_menu_windows()
    elif system == "Darwin":
        register_context_menu_mac()
    elif system == "Linux":
        register_context_menu_linux()
    else:
        raise NotImplementedError("Unsupported OS for context menu integration.")

def register_context_menu_windows():
    try:
        import winreg
    except ImportError:
        print("winreg module not available. Cannot register context menu on Windows.")
        return

    try:
        # Associate the .treefile extension with our custom file type.
        key_path = r"Software\Classes\.treefile"
        reg_key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, key_path)
        winreg.SetValue(reg_key, "", winreg.REG_SZ, "treefile_auto")
        winreg.CloseKey(reg_key)

        # Create the shell command for 'Unpack Treefile'.
        key_path = r"Software\Classes\treefile_auto\shell\Unpack Treefile\command"
        reg_key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, key_path)
        # Adjust the command as needed (assuming Python is on PATH).
        command = r'python -m treefile.cli --file "%1"'
        winreg.SetValue(reg_key, "", winreg.REG_SZ, command)
        winreg.CloseKey(reg_key)

        # Set the default icon for .treefile files.
        icon_path = get_icon_path("Windows")
        key_path = r"Software\Classes\treefile_auto\DefaultIcon"
        reg_key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, key_path)
        winreg.SetValue(reg_key, "", winreg.REG_SZ, icon_path)
        winreg.CloseKey(reg_key)

        print("Context menu and file icon registered successfully on Windows.")
    except Exception as e:
        print(f"Failed to register context menu or icon on Windows: {e}")

def register_context_menu_mac():
    icon_path = get_icon_path("Darwin")
    print("To register the context menu and file icon on macOS, please create an Automator service or use a tool like Platypus to create a service that runs:")
    print('python3 -m treefile.cli --file "$1"')
    print("\nThen, to assign the custom file icon, use the following command (ensure Xcode command-line tools are installed):")
    print(f'SetFile -a C "{icon_path}"')
    print("Refer to Apple’s guidelines for assigning custom icons.")

def register_context_menu_linux():
    icon_path = get_icon_path("Linux")
    print("To register the context menu and file icon on Linux, create a .desktop file with the following content:")
    print(f"""
[Desktop Entry]
Name=Unpack Treefile
Exec=python3 -m treefile.cli --file %f
Icon={icon_path}
MimeType=application/x-treefile;
Type=Application
Terminal=true
    """)
    print("Then update your MIME database accordingly.")

if __name__ == "__main__":
    register_context_menu()
