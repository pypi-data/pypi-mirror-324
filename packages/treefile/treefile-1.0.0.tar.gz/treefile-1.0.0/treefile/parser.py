import re

class Node:
    def __init__(self, name, is_dir, indent_level):
        self.name = name
        self.is_dir = is_dir
        self.indent_level = indent_level
        self.children = []
    
    def __repr__(self):
        return f"Node(name={self.name!r}, is_dir={self.is_dir}, indent={self.indent_level}, children={self.children})"

def get_indent_and_name(line):
    """
    Determine the indent level and clean file/folder name from a line.
    
    This function handles lines that include tree branch characters from the typical output of the "tree" command.
    It uses a regular expression to detect a branch marker pattern.
    
    For example:
      "├── token_itemize/"           -> indent level = 1, name = "token_itemize/"
      "│   ├── _init_.py"             -> indent level = 2, name = "_init_.py"
      "└── tests/"                   -> indent level = 1, name = "tests/"
      "    └── test_main.py"          -> indent level = 2, name = "test_main.py"
    """
    # Try to match a pattern with an optional leading space, followed by one or more branch markers and "── ", then the name.
    m = re.match(r'^( *)([│├└].*?── )(.*)$', line)
    if m:
        # Leading spaces (if any) before the branch markers.
        leading_spaces = len(m.group(1)) // 4
        # In the branch part, count every occurrence of a branch marker.
        branch_part = m.group(2)
        branch_count = sum(1 for ch in branch_part if ch in "│├└")
        indent_level = leading_spaces + branch_count
        name = m.group(3).strip()
        return indent_level, name
    else:
        # If no branch marker pattern is detected, use leading spaces only.
        stripped = line.lstrip(" ")
        indent_level = (len(line) - len(stripped)) // 4
        return indent_level, stripped.strip()

def parse_treefile(content):
    """
    Parse the .treefile content (a string) and return a list of top-level Node objects.
    
    Each non-empty line is processed with `get_indent_and_name` to determine its indent level and name.
    """
    lines = content.splitlines()
    nodes = []
    stack = []  # Stack holds tuples of (indent_level, node)

    for raw_line in lines:
        if not raw_line.strip():
            continue
        
        indent_level, name = get_indent_and_name(raw_line)
        
        # Determine if this is a directory: conventionally, its name ends with a slash.
        is_dir = name.endswith("/")
        node = Node(name, is_dir, indent_level)
        
        # Place the node in the tree structure based on its indent level.
        if not stack:
            nodes.append(node)
            stack.append((indent_level, node))
        else:
            # Pop from the stack until we find a node with a lower indent level.
            while stack and indent_level <= stack[-1][0]:
                stack.pop()
            if stack:
                parent = stack[-1][1]
                parent.children.append(node)
            else:
                nodes.append(node)
            stack.append((indent_level, node))
    return nodes
