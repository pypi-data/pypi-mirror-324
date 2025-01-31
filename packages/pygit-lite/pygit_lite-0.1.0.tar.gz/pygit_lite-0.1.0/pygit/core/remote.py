# pygit/core/remote.py
import os
import json
import shutil
import urllib.parse
from pathlib import Path

class RemoteManager:
    def __init__(self, repository):
        self.repo = repository
        self.remotes_file = os.path.join(repository.gitdir, 'config')

    def add_remote(self, name, url):
        """Add a new remote"""
        config = self._read_config()
        
        if 'remotes' not in config:
            config['remotes'] = {}
            
        config['remotes'][name] = {
            'url': url,
            'fetch': '+refs/heads/*:refs/remotes/' + name + '/*'
        }
        
        self._write_config(config)

    def remove_remote(self, name):
        """Remove a remote"""
        config = self._read_config()
        if 'remotes' in config and name in config['remotes']:
            del config['remotes'][name]
            self._write_config(config)

    def list_remotes(self):
        """List all configured remotes"""
        config = self._read_config()
        return config.get('remotes', {})

    def push(self, remote_name, branch_name):
        """Push objects to remote"""
        config = self._read_config()
        if 'remotes' not in config or remote_name not in config['remotes']:
            raise Exception(f"Remote '{remote_name}' not found")
            
        remote_url = config['remotes'][remote_name]['url']
        
        # Get local branch commit
        branch_path = os.path.join(self.repo.gitdir, 'refs', 'heads', branch_name)
        if not os.path.exists(branch_path):
            raise Exception(f"Branch '{branch_name}' not found")
            
        with open(branch_path, 'r') as f:
            local_commit = f.read().strip()
            
        # Collect objects to push
        objects_to_push = self._collect_objects_to_push(local_commit)
        
        # Push to remote (simplified for local filesystem)
        if remote_url.startswith('file://'):
            self._push_local(remote_url, branch_name, objects_to_push)
        else:
            self._push_http(remote_url, branch_name, objects_to_push)

    def pull(self, remote_name, branch_name):
        """Pull objects from remote"""
        config = self._read_config()
        if 'remotes' not in config or remote_name not in config['remotes']:
            raise Exception(f"Remote '{remote_name}' not found")
            
        remote_url = config['remotes'][remote_name]['url']
        
        # Fetch from remote
        if remote_url.startswith('file://'):
            self._pull_local(remote_url, branch_name)
        else:
            self._pull_http(remote_url, branch_name)

    def _read_config(self):
        """Read git config file"""
        if os.path.exists(self.remotes_file):
            with open(self.remotes_file, 'r') as f:
                return json.load(f)
        return {}

    def _write_config(self, config):
        """Write git config file"""
        with open(self.remotes_file, 'w') as f:
            json.dump(config, f, indent=4)

    def _collect_objects_to_push(self, commit_sha):
        """Collect all objects needed for push"""
        objects = set()
        queue = [commit_sha]
        
        while queue:
            sha = queue.pop(0)
            if sha in objects:
                continue
                
            objects.add(sha)
            obj = self.repo.get_object(sha)
            
            if hasattr(obj, 'parent_sha') and obj.parent_sha:
                queue.append(obj.parent_sha)
            if hasattr(obj, 'tree_sha'):
                queue.append(obj.tree_sha)
                
        return objects

    def _push_local(self, remote_url, branch_name, objects):
        """Push to local repository"""
        remote_path = urllib.parse.urlparse(remote_url).path
        remote_git_dir = os.path.join(remote_path, '.pygit')
        
        # Copy objects
        for obj_sha in objects:
            src = os.path.join(self.repo.gitdir, 'objects', obj_sha[:2], obj_sha[2:])
            dst = os.path.join(remote_git_dir, 'objects', obj_sha[:2], obj_sha[2:])
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            shutil.copy2(src, dst)
            
        # Update remote branch
        branch_path = os.path.join(self.repo.gitdir, 'refs', 'heads', branch_name)
        remote_branch_path = os.path.join(remote_git_dir, 'refs', 'heads', branch_name)
        os.makedirs(os.path.dirname(remote_branch_path), exist_ok=True)
        shutil.copy2(branch_path, remote_branch_path)

    def _push_http(self, remote_url, branch_name, objects):
        """Push to HTTP remote (simplified)"""
        # This would implement HTTP protocol for real remote repositories
        raise NotImplementedError("HTTP push not implemented")

    def _pull_local(self, remote_url, branch_name):
        """Pull from local repository"""
        remote_path = urllib.parse.urlparse(remote_url).path
        remote_git_dir = os.path.join(remote_path, '.pygit')
        
        # Copy objects
        remote_objects_dir = os.path.join(remote_git_dir, 'objects')
        for obj_dir in os.listdir(remote_objects_dir):
            obj_path = os.path.join(remote_objects_dir, obj_dir)
            if os.path.isdir(obj_path):
                for obj_file in os.listdir(obj_path):
                    src = os.path.join(obj_path, obj_file)
                    dst = os.path.join(self.repo.gitdir, 'objects', obj_dir, obj_file)
                    os.makedirs(os.path.dirname(dst), exist_ok=True)
                    if not os.path.exists(dst):
                        shutil.copy2(src, dst)
                        
        # Update local branch
        remote_branch_path = os.path.join(remote_git_dir, 'refs', 'heads', branch_name)
        if os.path.exists(remote_branch_path):
            branch_path = os.path.join(self.repo.gitdir, 'refs', 'heads', branch_name)
            os.makedirs(os.path.dirname(branch_path), exist_ok=True)
            shutil.copy2(remote_branch_path, branch_path)

    def _pull_http(self, remote_url, branch_name):
        """Pull from HTTP remote (simplified)"""
        # This would implement HTTP protocol for real remote repositories
        raise NotImplementedError("HTTP pull not implemented")
