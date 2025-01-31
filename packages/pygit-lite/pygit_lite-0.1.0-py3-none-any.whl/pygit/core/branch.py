# pygit/core/branch.py
import os
from pathlib import Path

class BranchManager:
    def __init__(self, repo_path):
        self.repo_path = repo_path
        self.refs_path = os.path.join(repo_path, '.pygit', 'refs', 'heads')
        self.head_path = os.path.join(repo_path, '.pygit', 'HEAD')
        
    def get_branch_commit(self, branch_name):
        """Get the commit SHA that a branch points to"""
        branch_path = os.path.join(self.refs_path, branch_name)
        if not os.path.exists(branch_path):
            return None
            
        with open(branch_path, 'r') as f:
            return f.read().strip()

    def create_branch(self, branch_name, start_point):
        """Create a new branch pointing to start_point"""
        branch_path = os.path.join(self.refs_path, branch_name)
        
        if os.path.exists(branch_path):
            raise Exception(f"Branch '{branch_name}' already exists")
            
        os.makedirs(os.path.dirname(branch_path), exist_ok=True)
        with open(branch_path, 'w') as f:
            f.write(start_point)

    def get_current_branch(self):
        """Get the name of the current branch"""
        if not os.path.exists(self.head_path):
            return None
            
        with open(self.head_path, 'r') as f:
            content = f.read().strip()
            if content.startswith('ref: refs/heads/'):
                return content.replace('ref: refs/heads/', '')
        return None

    def list_branches(self):
        """List all branches"""
        branches = []
        current = self.get_current_branch()
        
        for branch_file in Path(self.refs_path).glob('*'):
            branch_name = branch_file.name
            branches.append({
                'name': branch_name,
                'current': branch_name == current
            })
        
        return branches

    def switch_branch(self, branch_name):
        """Switch to a different branch"""
        branch_path = os.path.join(self.refs_path, branch_name)
        
        if not os.path.exists(branch_path):
            raise Exception(f"Branch '{branch_name}' does not exist")
            
        with open(self.head_path, 'w') as f:
            f.write(f'ref: refs/heads/{branch_name}')
