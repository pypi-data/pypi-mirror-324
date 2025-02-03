import unittest
from treefile.parser import parse_treefile

class TestParser(unittest.TestCase):
    def test_simple_tree(self):
        content = """
token-itemize/
    token_itemize/
        __init__.py
        cli.py
    tests/
        test_example.py
"""
        nodes = parse_treefile(content)
        # There should be one top-level node: "token-itemize/"
        self.assertEqual(len(nodes), 1)
        root = nodes[0]
        self.assertEqual(root.name, "token-itemize/")
        self.assertTrue(root.is_dir)
        # Check that root has two children: "token_itemize/" and "tests/"
        self.assertEqual(len(root.children), 2)
        names = sorted(child.name for child in root.children)
        self.assertEqual(names, ["tests/", "token_itemize/"])

if __name__ == "__main__":
    unittest.main()
