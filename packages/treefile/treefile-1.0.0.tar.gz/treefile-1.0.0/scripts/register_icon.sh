#!/bin/bash
# This script registers the context menu and file icon for .treefile files on macOS/Linux. (Make sure to mark this file as executable by running: chmod +x scripts/register_icon.sh.)
python3 -c "import treefile.context_menu as cm; cm.register_context_menu()"
