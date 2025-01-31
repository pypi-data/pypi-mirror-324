# pygit/core/merge.py
import os
from collections import defaultdict

class MergeConflict(Exception):
    pass

class MergeManager:
    def __init__(self, repository):
        self.repo = repository

    def find_common_ancestor(self, commit1_sha, commit2_sha):
        """Find the most recent common ancestor of two commits"""
        commit1_history = self._get_commit_history(commit1_sha)
        commit2_history = self._get_commit_history(commit2_sha)
        
        for sha in commit1_history:
            if sha in commit2_history:
                return sha
        
        return None

    def _get_commit_history(self, start_sha):
        """Get all ancestor commits of a given commit"""
        history = set()
        queue = [start_sha]
        
        while queue:
            current_sha = queue.pop(0)
            if current_sha in history:
                continue
                
            history.add(current_sha)
            commit = self.repo.get_commit(current_sha)
            if commit and commit.parent_sha:
                queue.append(commit.parent_sha)
                
        return history

    def merge_trees(self, base_tree, ours_tree, theirs_tree):
        """Merge two trees with their common ancestor"""
        merged = {}
        conflicts = []
        
        # Collect all paths
        all_paths = set()
        for tree in (base_tree, ours_tree, theirs_tree):
            if tree:
                all_paths.update(tree.data.keys())

        for path in all_paths:
            base_sha = base_tree.data.get(path) if base_tree else None
            ours_sha = ours_tree.data.get(path) if ours_tree else None
            theirs_sha = theirs_tree.data.get(path) if theirs_tree else None
            
            # No conflict cases
            if ours_sha == theirs_sha:
                if ours_sha:
                    merged[path] = ours_sha
                continue
                
            if base_sha == ours_sha and theirs_sha:
                merged[path] = theirs_sha
                continue
                
            if base_sha == theirs_sha and ours_sha:
                merged[path] = ours_sha
                continue
                
            # Conflict case
            conflicts.append({
                'path': path,
                'base': base_sha,
                'ours': ours_sha,
                'theirs': theirs_sha
            })

        return merged, conflicts

    def create_conflict_file(self, path, base_content, ours_content, theirs_content):
        """Create a file with conflict markers"""
        content = []
        content.append("<<<<<<< HEAD")
        content.append(ours_content or '')
        content.append("=======")
        content.append(theirs_content or '')
        content.append(">>>>>>> MERGE_HEAD")
        
        return '\n'.join(content)
