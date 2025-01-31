# pygit/cli.py
import os
import argparse
from .core.repository import Repository
from .core.merge import MergeConflict

def main():
    parser = argparse.ArgumentParser(description='PyGit - A Python implementation of Git')
    subparsers = parser.add_subparsers(dest='command')
    
    # init command
    init_parser = subparsers.add_parser('init', help='Initialize a new repository')
    
    # add command
    add_parser = subparsers.add_parser('add', help='Add file contents to the staging area')
    add_parser.add_argument('files', nargs='+', help='Files to add')
    
    # status command
    status_parser = subparsers.add_parser('status', help='Show the working tree status')

    # commit command
    commit_parser = subparsers.add_parser('commit', help='Record changes to the repository')
    commit_parser.add_argument('-m', '--message', required=True, help='Commit message')
    commit_parser.add_argument('--author', help='Author of the commit')
    
    # log command
    log_parser = subparsers.add_parser('log', help='Show commit logs')
    log_parser.add_argument('--max-count', type=int, help='Limit number of commits to show')

    # branch commands
    branch_parser = subparsers.add_parser('branch', help='List, create, or delete branches')
    branch_parser.add_argument('name', nargs='?', help='The name of the branch to create')
    
    # checkout command
    checkout_parser = subparsers.add_parser('checkout', help='Switch branches')
    checkout_parser.add_argument('branch_name', help='Branch to switch to')

    # diff command
    diff_parser = subparsers.add_parser('diff', help='Show changes between commits, commit and working tree, etc')
    diff_parser.add_argument('--staged', action='store_true', help='Show difference between staged changes and last commit')
    
    # merge command
    merge_parser = subparsers.add_parser('merge', help='Join two or more development histories together')
    merge_parser.add_argument('branch', help='Branch to merge into current branch')
    
    # remote commands
    remote_parser = subparsers.add_parser('remote', help='Manage set of tracked repositories')
    remote_subparsers = remote_parser.add_subparsers(dest='remote_command')
    
    remote_add = remote_subparsers.add_parser('add', help='Add a remote')
    remote_add.add_argument('name', help='Name of the remote')
    remote_add.add_argument('url', help='URL of the remote')
    
    remote_remove = remote_subparsers.add_parser('remove', help='Remove a remote')
    remote_remove.add_argument('name', help='Name of the remote to remove')
    
    remote_list = remote_subparsers.add_parser('list', help='List remotes')
    
    # push command
    push_parser = subparsers.add_parser('push', help='Update remote refs along with associated objects')
    push_parser.add_argument('remote', help='Name of the remote')
    push_parser.add_argument('branch', help='Branch to push')
    
    # pull command
    pull_parser = subparsers.add_parser('pull', help='Fetch from and integrate with another repository')
    pull_parser.add_argument('remote', help='Name of the remote')
    pull_parser.add_argument('branch', help='Branch to pull')
  
    args = parser.parse_args()
    repo = Repository(os.getcwd())

    if args.command == 'init':
        try:
            repo.init()
            print(f'Initialized empty PyGit repository in {repo.gitdir}')
        except Exception as e:
            print(f'Error: {str(e)}')
            return 1
            
    elif args.command == 'add':
        try:
            for file in args.files:
                sha = repo.stage_file(file)
                print(f'Added {file} ({sha})')
        except Exception as e:
            print(f'Error: {str(e)}')
            return 1
            
    elif args.command == 'status':
        try:
            status = repo.status()
            print("\nChanges to be committed:")
            for file in status['staged']:
                print(f"\tmodified: {file}")
            
            print("\nUntracked files:")
            for file in status['untracked']:
                print(f"\t{file}")
        except Exception as e:
            print(f'Error: {str(e)}')
            return 1
        
    elif args.command == 'commit':
        try:
            commit_sha = repo.commit(args.message, args.author)
            print(f'[master {commit_sha[:7]}] {args.message}')
        except Exception as e:
            print(f'Error: {str(e)}')
            return 1
    
    elif args.command == 'log':
        try:
            commits = repo.log()
            if args.max_count:
                commits = commits[:args.max_count]
                
            if not commits:
                print("No commits yet")
                return 0
                
            for commit in commits:
                print(repo.format_commit_log(commit))
                
        except Exception as e:
            print(f'Error: {str(e)}')
            return 1

    elif args.command == 'branch':
        try:
            if args.name:
                repo.create_branch(args.name)
                print(f"Created branch '{args.name}'")
            else:
                branches = repo.list_branches()
                for branch in branches:
                    prefix = '* ' if branch['current'] else '  '
                    print(f"{prefix}{branch['name']}")
        except Exception as e:
            print(f'Error: {str(e)}')
            return 1
            
    elif args.command == 'checkout':
        try:
            repo.switch_branch(args.branch_name)
            print(f"Switched to branch '{args.branch_name}'")
        except Exception as e:
            print(f'Error: {str(e)}')
            return 1

    elif args.command == 'diff':
        try:
            diffs = repo.diff(staged=args.staged)
            if not diffs:
                print("No changes")
                return 0
                
            for diff_entry in diffs:
                if diff_entry.status == 'added':
                    print(f'New file: {diff_entry.path}')
                elif diff_entry.status == 'modified':
                    print(f'Modified: {diff_entry.path}')
                
                diff_lines = repo.diff_manager.compare_files(
                    diff_entry.old_content,
                    diff_entry.new_content,
                    diff_entry.path
                )
                
                if diff_lines:
                    print(''.join(diff_lines))
                print()
        except Exception as e:
            print(f'Error: {str(e)}')
            return 1

    elif args.command == 'merge':
        try:
            repo.merge(args.branch)
            print(f"Successfully merged branch '{args.branch}'")
        except MergeConflict as e:
            print(f"Merge conflict: {str(e)}")
            print("Fix conflicts and commit the result.")
            return 1
        except Exception as e:
            print(f'Error: {str(e)}')
            return 1

    elif args.command == 'remote':
        try:
            if args.remote_command == 'add':
                repo.add_remote(args.name, args.url)
                print(f"Added remote '{args.name}' ({args.url})")
            elif args.remote_command == 'remove':
                repo.remove_remote(args.name)
                print(f"Removed remote '{args.name}'")
            elif args.remote_command == 'list':
                remotes = repo.list_remotes()
                for name, info in remotes.items():
                    print(f"{name}\t{info['url']}")
        except Exception as e:
            print(f'Error: {str(e)}')
            return 1
            
    elif args.command == 'push':
        try:
            repo.push(args.remote, args.branch)
            print(f"Pushed to {args.remote}/{args.branch}")
        except Exception as e:
            print(f'Error: {str(e)}')
            return 1
            
    elif args.command == 'pull':
        try:
            repo.pull(args.remote, args.branch)
            print(f"Pulled from {args.remote}/{args.branch}")
        except Exception as e:
            print(f'Error: {str(e)}')
            return 1

    return 0

    

if __name__ == '__main__':
    main()
