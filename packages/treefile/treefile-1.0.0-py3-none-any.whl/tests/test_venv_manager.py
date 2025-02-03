import unittest
import tempfile
from pathlib import Path
from treefile.venv_manager import create_virtualenv

class TestVenvManager(unittest.TestCase):
    def test_create_virtualenv_dry_run(self):
        with tempfile.TemporaryDirectory() as tmpdirname:
            base_path = Path(tmpdirname)
            venv_name = ".venv_test"
            venv_path = create_virtualenv(base_path, venv_name, "python", dry_run=True)
            self.assertEqual(venv_path, base_path / venv_name)
            # In dry-run mode, the venv is not actually created.
            self.assertFalse(venv_path.exists())

if __name__ == "__main__":
    unittest.main()
