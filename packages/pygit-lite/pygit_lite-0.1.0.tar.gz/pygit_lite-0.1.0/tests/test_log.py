# tests/test_log.py
import unittest
import os
import shutil
from pygit.core.repository import Repository

class TestLog(unittest.TestCase):
    def setUp(self):
        self.test_dir = "test_repo"
        os.makedirs(self.test_dir, exist_ok=True)
        os.chdir(self.test_dir)
        self.repo = Repository(os.getcwd())
        self.repo.init()

    def tearDown(self):
        os.chdir("..")
        shutil.rmtree(self.test_dir)

    def test_log_empty_repo(self):
        logs = self.repo.log()
        self.assertEqual(len(logs), 0)

    def test_log_single_commit(self):
        # Create a test file
        with open("test.txt", "w") as f:
            f.write("test content")
        
        self.repo.stage_file("test.txt")
        commit_sha = self.repo.commit("Test commit", "Test Author <test@example.com>")
        
        logs = self.repo.log()
        self.assertEqual(len(logs), 1)
        self.assertEqual(logs[0]['sha'], commit_sha)
        self.assertEqual(logs[0]['message'], "Test commit")

if __name__ == '__main__':
    unittest.main()
