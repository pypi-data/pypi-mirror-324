import unittest
import tempfile
from pathlib import Path
from treefile.core import generate_tree
from treefile.parser import parse_treefile

class TestCore(unittest.TestCase):
    def test_generate_tree(self):
        content = """
project/
    src/
        main.py
    README.md
"""
        nodes = parse_treefile(content)
        with tempfile.TemporaryDirectory() as tmpdirname:
            base_path = Path(tmpdirname)
            generate_tree(nodes, base_path, dry_run=False, force=True)
            project_dir = base_path / "project"
            self.assertTrue(project_dir.exists())
            self.assertTrue((project_dir / "src").exists())
            self.assertTrue((project_dir / "src" / "main.py").exists())
            self.assertTrue((project_dir / "README.md").exists())

if __name__ == "__main__":
    unittest.main()
