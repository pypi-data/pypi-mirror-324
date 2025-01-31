# tests/test_merge.py
import unittest
import os
import shutil
from pygit.core.repository import Repository
from pygit.core.merge import MergeConflict

class TestMerge(unittest.TestCase):
    def setUp(self):
        self.test_dir = "test_repo"
        os.makedirs(self.test_dir, exist_ok=True)
        os.chdir(self.test_dir)
        self.repo = Repository(os.getcwd())
        self.repo.init()

    def tearDown(self):
        os.chdir("..")
        shutil.rmtree(self.test_dir)

    def test_simple_merge(self):
        # Create initial commit
        with open("test.txt", "w") as f:
            f.write("initial content\n")
        self.repo.stage_file("test.txt")
        self.repo.commit("Initial commit", "Test Author <test@example.com>")
        
        # Create and switch to new branch
        self.repo.create_branch("feature")
        self.repo.switch_branch("feature")
        
        # Make changes in feature branch
        with open("test.txt", "w") as f:
            f.write("feature content\n")
        self.repo.stage_file("test.txt")
        self.repo.commit("Feature commit", "Test Author <test@example.com>")
        
        # Switch back to master and merge
        self.repo.switch_branch("master")
        self.repo.merge("feature")
        
        # Verify merge
        with open("test.txt", "r") as f:
            content = f.read()
        self.assertEqual(content, "feature content\n")

    def test_merge_conflict(self):
        # Similar setup but with conflicting changes
        # ... (implement test for merge conflicts)
        pass

if __name__ == '__main__':
    unittest.main()
