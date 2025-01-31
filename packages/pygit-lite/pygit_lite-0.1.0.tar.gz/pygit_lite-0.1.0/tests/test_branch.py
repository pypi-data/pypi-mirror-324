# tests/test_branch.py
import unittest
import os
import shutil
from pygit.core.repository import Repository

class TestBranch(unittest.TestCase):
    def setUp(self):
        self.test_dir = "test_repo"
        os.makedirs(self.test_dir, exist_ok=True)
        os.chdir(self.test_dir)
        self.repo = Repository(os.getcwd())
        self.repo.init()

    def tearDown(self):
        os.chdir("..")
        shutil.rmtree(self.test_dir)

    def test_create_branch(self):
        # Create initial commit
        with open("test.txt", "w") as f:
            f.write("test content")
        self.repo.stage_file("test.txt")
        self.repo.commit("Initial commit", "Test Author <test@example.com>")
        
        # Create and verify new branch
        self.repo.create_branch("test-branch")
        branches = self.repo.list_branches()
        branch_names = [b['name'] for b in branches]
        self.assertIn("test-branch", branch_names)

    def test_switch_branch(self):
        # Create initial commit and branch
        with open("test.txt", "w") as f:
            f.write("test content")
        self.repo.stage_file("test.txt")
        self.repo.commit("Initial commit", "Test Author <test@example.com>")
        self.repo.create_branch("test-branch")
        
        # Switch and verify
        self.repo.switch_branch("test-branch")
        current_branch = self.repo.branch_manager.get_current_branch()
        self.assertEqual(current_branch, "test-branch")

if __name__ == '__main__':
    unittest.main()
