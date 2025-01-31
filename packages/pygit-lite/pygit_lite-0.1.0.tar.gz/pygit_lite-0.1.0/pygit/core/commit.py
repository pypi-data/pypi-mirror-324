# pygit/core/commit.py
import time
import json

class Commit:
    def __init__(self, tree_sha, parent_sha, message, author=None):
        self.tree_sha = tree_sha
        self.parent_sha = parent_sha
        self.message = message
        self.author = author or "Unknown <unknown@example.com>"
        self.timestamp = int(time.time())

    def serialize(self):
        """Convert commit data to JSON format"""
        commit_data = {
            "tree": self.tree_sha,
            "parent": self.parent_sha,
            "author": self.author,
            "timestamp": self.timestamp,
            "message": self.message
        }
        return json.dumps(commit_data).encode()

    @classmethod
    def deserialize(cls, data):
        """Create a commit object from JSON data"""
        commit_data = json.loads(data.decode())
        commit = cls(
            tree_sha=commit_data["tree"],
            parent_sha=commit_data["parent"],
            message=commit_data["message"],
            author=commit_data["author"]
        )
        commit.timestamp = commit_data["timestamp"]
        return commit
