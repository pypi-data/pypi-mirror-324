# tests/test_remote.py
import unittest
import os
import shutil
from pygit.core.repository import Repository

class TestRemote(unittest.TestCase):
    def setUp(self):
        self.test_dir = "test_repo"
        self.remote_dir = "remote_repo"
        os.makedirs(self.test_dir, exist_ok=True)
        os.makedirs(self.remote_dir, exist_ok=True)
        
        # Initialize local repo
        os.chdir(self.test_dir)
        self.repo = Repository(os.getcwd())
        self.repo.init()
        
        # Initialize remote repo
        os.chdir("../"+self.remote_dir)
        self.remote_repo = Repository(os.getcwd())
        self.remote_repo.init()
        
        # Back to local repo
        os.chdir("../"+self.test_dir)

    def tearDown(self):
        os.chdir("..")
        shutil.rmtree(self.test_dir)
        shutil.rmtree(self.remote_dir)

    def test_add_remote(self):
        remote_url = "file://../remote_repo"
        self.repo.add_remote("origin", remote_url)
        remotes = self.repo.list_remotes()
        self.assertIn("origin", remotes)
        self.assertEqual(remotes["origin"]["url"], remote_url)

    def test_push_pull(self):
        # Add remote
        remote_url = "file://../remote_repo"
        self.repo.add_remote("origin", remote_url)
        
        # Create and commit a file
        with open("test.txt", "w") as f:
            f.write("test content")
        self.repo.stage_file("test.txt")
        self.repo.commit("Initial commit", "Test Author <test@example.com>")
        
        # Push to remote
        self.repo.push("origin", "master")
        
        # Verify in remote
        os.chdir("../"+self.remote_dir)
        with open("test.txt", "r") as f:
            content = f.read()
        self.assertEqual(content, "test content")

if __name__ == '__main__':
    unittest.main()
