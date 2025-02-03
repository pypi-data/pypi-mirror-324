@echo off
REM This script registers the context menu and file icon for .treefile files on Windows.
python -c "import treefile.context_menu as cm; cm.register_context_menu()"
pause
