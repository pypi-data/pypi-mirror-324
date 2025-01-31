# tests/test_diff.py
import unittest
import os
import shutil
from pygit.core.repository import Repository

class TestDiff(unittest.TestCase):
    def setUp(self):
        self.test_dir = "test_repo"
        os.makedirs(self.test_dir, exist_ok=True)
        os.chdir(self.test_dir)
        self.repo = Repository(os.getcwd())
        self.repo.init()

    def tearDown(self):
        os.chdir("..")
        shutil.rmtree(self.test_dir)

    def test_diff_new_file(self):
        # Create a new file
        with open("test.txt", "w") as f:
            f.write("test content\n")
        
        diffs = self.repo.diff()
        self.assertEqual(len(diffs), 1)
        self.assertEqual(diffs[0].status, 'added')
        self.assertEqual(diffs[0].path, 'test.txt')

    def test_diff_modified_file(self):
        # Create and stage initial file
        with open("test.txt", "w") as f:
            f.write("initial content\n")
        self.repo.stage_file("test.txt")
        self.repo.commit("Initial commit", "Test Author <test@example.com>")
        
        # Modify file
        with open("test.txt", "w") as f:
            f.write("modified content\n")
        
        diffs = self.repo.diff()
        self.assertEqual(len(diffs), 1)
        self.assertEqual(diffs[0].status, 'modified')
        self.assertEqual(diffs[0].path, 'test.txt')

if __name__ == '__main__':
    unittest.main()
