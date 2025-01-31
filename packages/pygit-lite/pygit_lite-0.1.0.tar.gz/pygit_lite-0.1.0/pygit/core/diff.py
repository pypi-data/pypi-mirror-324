# pygit/core/diff.py
from difflib import unified_diff
import os

class DiffEntry:
    def __init__(self, path, status, old_content="", new_content=""):
        self.path = path
        self.status = status  # 'modified', 'added', 'deleted'
        self.old_content = old_content
        self.new_content = new_content

class DiffManager:
    def __init__(self, repository):
        self.repo = repository

    def get_file_content(self, sha, path):
        """Get file content from a specific commit"""
        if not sha:
            return ""
        try:
            blob = self.repo.get_blob(sha)
            return blob.data.decode('utf-8', errors='replace')
        except:
            return ""

    def compare_files(self, old_content, new_content, path):
        """Compare two versions of a file"""
        if old_content == new_content:
            return []
            
        old_lines = old_content.splitlines(keepends=True)
        new_lines = new_content.splitlines(keepends=True)
        
        return list(unified_diff(
            old_lines, new_lines,
            fromfile=f'a/{path}',
            tofile=f'b/{path}',
            lineterm=''
        ))

    def diff_working_tree(self, staged=False):
        """Compare working tree with staged/committed files"""
        diffs = []
        staging = self.repo._read_staging()
        
        # Get all files in working directory
        for root, _, files in os.walk(self.repo.worktree):
            if '.pygit' in root:
                continue
                
            for file in files:
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, self.repo.worktree)
                
                try:
                    with open(full_path, 'r', encoding='utf-8') as f:
                        working_content = f.read()
                except UnicodeDecodeError:
                    continue  # Skip binary files
                
                if rel_path in staging:
                    # File is staged/tracked
                    old_content = self.get_file_content(
                        staging[rel_path]['sha'], rel_path)
                    if working_content != old_content:
                        diffs.append(DiffEntry(
                            rel_path,
                            'modified',
                            old_content,
                            working_content
                        ))
                else:
                    # Untracked file
                    diffs.append(DiffEntry(
                        rel_path,
                        'added',
                        "",
                        working_content
                    ))
        
        return diffs
