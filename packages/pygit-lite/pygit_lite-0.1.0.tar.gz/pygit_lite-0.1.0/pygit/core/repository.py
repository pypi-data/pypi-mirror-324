# pygit/core/repository.py

import os
import hashlib
import json
import zlib
from datetime import datetime
from pathlib import Path
from .objects import hash_object, Blob
from .commit import Commit
from .objects import hash_object, read_object, Tree
from datetime import datetime
from .branch import BranchManager
from .diff import DiffManager
from .merge import MergeManager, MergeConflict
from .remote import RemoteManager
import time

class Repository:
    def __init__(self, path):
        self.worktree = path
        self.gitdir = os.path.join(path, '.pygit')
        self.staging_file = os.path.join(self.gitdir, 'staging', 'index')
        self.branch_manager = BranchManager(path)
        self.diff_manager = DiffManager(self)
        self.merge_manager = MergeManager(self)
        self.remote_manager = RemoteManager(self)
   
    def init(self):
        """Initialize a new PyGit repository"""
        if os.path.exists(self.gitdir):
            raise Exception('Repository already exists')
            
        # Create directory structure
        os.makedirs(self.gitdir)
        for dir in ['objects', 'refs/heads', 'staging']:
            os.makedirs(os.path.join(self.gitdir, dir))
            
        # Create default config
        config = {
            'repository': {
                'version': '1.0',
                'created_at': datetime.now().isoformat()
            }
        }
        
        # Write config file
        with open(os.path.join(self.gitdir, 'config'), 'w') as f:
            json.dump(config, f, indent=4)
            
        # Create HEAD file pointing to master branch
        with open(os.path.join(self.gitdir, 'HEAD'), 'w') as f:
            f.write('ref: refs/heads/master')
            
        return self

    def stage_file(self, filepath):
        """Add a file to the staging area"""
        abs_path = os.path.join(self.worktree, filepath)
        
        if not os.path.exists(abs_path):
            raise Exception(f"File {filepath} does not exist")
            
        with open(abs_path, 'rb') as f:
            data = f.read()
            
        # Hash the file content
        sha = hash_object(data, 'blob', write=True)
        
        # Add to staging
        staging = self._read_staging()
        staging[filepath] = {
            'sha': sha,
            'timestamp': datetime.now().isoformat()
        }
        self._write_staging(staging)
        
        return sha

    def _read_staging(self):
        """Read the staging area"""
        if os.path.exists(self.staging_file):
            with open(self.staging_file, 'r') as f:
                return json.load(f)
        return {}

    def _write_staging(self, staging):
        """Write to the staging area"""
        os.makedirs(os.path.dirname(self.staging_file), exist_ok=True)
        with open(self.staging_file, 'w') as f:
            json.dump(staging, f, indent=4)

    def status(self):
        """Get the status of the working directory"""
        staged_files = self._read_staging()
        status = {
            'staged': [],
            'modified': [],
            'untracked': []
        }
        
        # Check all files in working directory
        for root, _, files in os.walk(self.worktree):
            if '.pygit' in root:
                continue
                
            for file in files:
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, self.worktree)
                
                if rel_path in staged_files:
                    status['staged'].append(rel_path)
                else:
                    status['untracked'].append(rel_path)
                    
        return status
    
    def create_tree(self):
        """Create a tree object from the current staging area"""
        staging = self._read_staging()
        tree_data = {}
        
        for path, info in staging.items():
            tree_data[path] = info['sha']
            
        tree = Tree()
        tree.data = tree_data
        return hash_object(tree.serialize(), 'tree', write=True)

    def get_head(self):
        """Get the current HEAD commit SHA"""
        head_path = os.path.join(self.gitdir, 'HEAD')
        if not os.path.exists(head_path):
            return None
            
        with open(head_path, 'r') as f:
            ref = f.read().strip()
            if ref.startswith('ref: '):
                ref_path = os.path.join(self.gitdir, ref.split(': ')[1])
                if os.path.exists(ref_path):
                    with open(ref_path, 'r') as ref_file:
                        return ref_file.read().strip()
        return None

    def commit(self, message, author=None, parent_sha=None):
        """Create a new commit"""
        # Create tree from staging
        tree_sha = self.create_tree()
        
        # Get parent commit if not provided
        if parent_sha is None:
            parent_sha = self.get_head()
        
        # Create commit object
        commit = Commit(
            tree_sha=tree_sha,
            parent_sha=parent_sha,
            message=message,
            author=author
        )
        
        # Hash and store commit
        commit_sha = hash_object(commit.serialize(), 'commit', write=True)
        
        # Update HEAD
        master_path = os.path.join(self.gitdir, 'refs', 'heads', 'master')
        os.makedirs(os.path.dirname(master_path), exist_ok=True)
        with open(master_path, 'w') as f:
            f.write(commit_sha)
            
        # Clear staging
        self._write_staging({})
        
        return commit_sha

    def get_commit(self, sha):
        """Get a commit object by its SHA"""
        if not sha:
            return None
        return read_object(sha)

    def log(self, start_sha=None):
        """Get commit history starting from given SHA (or HEAD if None)"""
        if start_sha is None:
            start_sha = self.get_head()
            
        commits = []
        current_sha = start_sha
        
        while current_sha:
            commit = self.get_commit(current_sha)
            if not commit:
                break
                
            commits.append({
                'sha': current_sha,
                'message': commit.message,
                'author': commit.author,
                'timestamp': commit.timestamp,
                'parent': commit.parent_sha
            })
            
            current_sha = commit.parent_sha
            
        return commits

    def format_commit_log(self, commit_info):
        """Format a commit for display"""
        date_str = datetime.fromtimestamp(commit_info['timestamp']).strftime('%Y-%m-%d %H:%M:%S')
        return (
            f"commit {commit_info['sha']}\n"
            f"Author: {commit_info['author']}\n"
            f"Date:   {date_str}\n"
            f"\n    {commit_info['message']}\n"
        )

    def create_branch(self, branch_name):
        """Create a new branch at current HEAD"""
        current_sha = self.get_head()
        if not current_sha:
            raise Exception("Cannot create branch: no commits yet")
        
        self.branch_manager.create_branch(branch_name, current_sha)

    def list_branches(self):
        """List all branches"""
        return self.branch_manager.list_branches()

    def switch_branch(self, branch_name):
        """Switch to a different branch"""
        self.branch_manager.switch_branch(branch_name)

    def get_blob(self, sha):
        """Get a blob object by its SHA"""
        return read_object(sha)

    def diff(self, staged=False):
        """Show changes between working tree and staged/committed files"""
        return self.diff_manager.diff_working_tree(staged)

    def format_diff(self, diff_entry):
        """Format a diff entry for display"""
        output = []
        
        if diff_entry.status == 'added':
            output.append(f"New file: {diff_entry.path}")
        elif diff_entry.status == 'modified':
            output.append(f"Modified: {diff_entry.path}")
        
        diff_lines = self.diff_manager.compare_files(
            diff_entry.old_content,
            diff_entry.new_content,
            diff_entry.path
        )
        
        if diff_lines:
            output.extend(diff_lines)
            
        return '\n'.join(output) if output else ""

    def merge(self, branch_name):
        """Merge another branch into current branch"""
        current_branch = self.branch_manager.get_current_branch()
        if not current_branch:
            raise Exception("Not on any branch")
            
        # Get commit SHAs
        current_sha = self.get_head()
        other_sha = self.branch_manager.get_branch_commit(branch_name)
        if not other_sha:
            raise Exception(f"Branch '{branch_name}' not found")
            
        # Find common ancestor
        base_sha = self.merge_manager.find_common_ancestor(current_sha, other_sha)
        if not base_sha:
            raise Exception("No common ancestor found")
            
        # Get trees
        base_commit = self.get_commit(base_sha)
        current_commit = self.get_commit(current_sha)
        other_commit = self.get_commit(other_sha)
        
        base_tree = self.get_tree(base_commit.tree_sha) if base_commit else Tree()
        current_tree = self.get_tree(current_commit.tree_sha) if current_commit else Tree()
        other_tree = self.get_tree(other_commit.tree_sha) if other_commit else Tree()
        
        # Merge trees
        merged_tree, conflicts = self.merge_manager.merge_trees(
            base_tree, current_tree, other_tree)
            
        if conflicts:
            # Handle conflicts
            for conflict in conflicts:
                path = conflict['path']
                base_content = self.get_blob_content(conflict['base'])
                ours_content = self.get_blob_content(conflict['ours'])
                theirs_content = self.get_blob_content(conflict['theirs'])
                
                conflict_content = self.merge_manager.create_conflict_file(
                    path, base_content, ours_content, theirs_content)
                    
                # Write conflict file
                full_path = os.path.join(self.worktree, path)
                os.makedirs(os.path.dirname(full_path), exist_ok=True)
                with open(full_path, 'w') as f:
                    f.write(conflict_content)
                    
            raise MergeConflict("Automatic merge failed. Fix conflicts and commit the result.")
            
        # Create merge commit
        merge_message = f"Merge branch '{branch_name}' into {current_branch}"
        self.commit(merge_message, parent_sha=other_sha)
        
        return True

    def get_tree(self, sha):
        """Get a tree object by its SHA"""
        if not sha:
            return Tree()
        return read_object(sha)

    def get_blob_content(self, sha):
        """Get blob content as string"""
        if not sha:
            return ""
        try:
            blob = self.get_blob(sha)
            return blob.data.decode('utf-8')
        except:
            return ""

# pygit/core/repository.py

    def get_object(self, sha):
        """Get any object from the repository by SHA"""
        if not sha:
            return None
        
        try:
            path = os.path.join(self.gitdir, 'objects', sha[:2], sha[2:])
            if not os.path.exists(path):
                raise Exception(f"Object {sha} not found")
                
            with open(path, 'rb') as f:
                raw = zlib.decompress(f.read())
                
            # Parse object type and data
            x = raw.find(b'\x00')
            if x < 0:
                raise Exception("Invalid object format")
                
            fmt = raw[0:x].decode().split()[0]
            data = raw[x+1:]
            
            if fmt == 'blob':
                return Blob(data)
            elif fmt == 'tree':
                tree = Tree()
                tree.deserialize(data)
                return tree
            elif fmt == 'commit':
                from .commit import Commit
                return Commit.deserialize(data)
            else:
                raise Exception(f"Unknown object type {fmt}")
        except Exception as e:
            raise Exception(f"Error reading object {sha}: {str(e)}")

    def add_remote(self, name, url):
        """Add a new remote repository"""
        return self.remote_manager.add_remote(name, url)

    def remove_remote(self, name):
        """Remove a remote repository"""
        return self.remote_manager.remove_remote(name)

    def list_remotes(self):
        """List all remote repositories"""
        return self.remote_manager.list_remotes()

    def push(self, remote_name, branch_name):
        """Push to remote repository"""
        return self.remote_manager.push(remote_name, branch_name)

    def pull(self, remote_name, branch_name):
        """Pull from remote repository"""
        return self.remote_manager.pull(remote_name, branch_name)
 
    def hash_object(self, data, obj_type, write=True):
        """Hash and optionally write an object to the repository"""
        header = f"{obj_type} {len(data)}".encode()
        full_data = header + b'\x00' + (data if isinstance(data, bytes) else data.encode())
        sha1 = hashlib.sha1(full_data).hexdigest()[1][4]
        
        if write:
            path = os.path.join(self.gitdir, 'objects', sha1[:2], sha1[2:])
            if not os.path.exists(path):
                os.makedirs(os.path.dirname(path), exist_ok=True)
                with open(path, 'wb') as f:
                    f.write(zlib.compress(full_data))
        
        return sha1
