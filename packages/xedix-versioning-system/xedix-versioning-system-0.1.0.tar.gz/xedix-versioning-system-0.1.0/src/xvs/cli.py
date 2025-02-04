import argparse
import sys
from .core import XVSCore

def main():
    parser = argparse.ArgumentParser(description='XVS Version Control System')
    subparsers = parser.add_subparsers(dest='command', help='Commands')

    # Branch command
    branch_parser = subparsers.add_parser('branch', help='Switch to or create a branch')
    branch_parser.add_argument('name', help='Branch name')

    # Commit command
    commit_parser = subparsers.add_parser('commit', help='Commit changes')
    commit_parser.add_argument('files', help='Comma-separated list of files')
    commit_parser.add_argument('message', help='Commit message')

    # Stage command
    stage_parser = subparsers.add_parser('stage', help='Stage changes')
    stage_parser.add_argument('files', help='Comma-separated list of files')
    stage_parser.add_argument('message', help='Stage message')
    
    # Status command
    status_parser = subparsers.add_parser('status', help='Show status of working directory')
    
    # Init command
    init_parser = subparsers.add_parser('init', help='Initialize a new repository')

    args = parser.parse_args()

    if args.command == 'branch':
        XVSCore.handle_branch(args.name)
    elif args.command == 'commit':
        XVSCore.handle_commit(args.files, args.message)
    elif args.command == 'stage':
        XVSCore.handle_stage(args.files, args.message)
    elif args.command == 'status':
        XVSCore.handle_status()
    elif args.command == 'init':
        XVSCore.handle_init()
    else:
        parser.print_help()
        sys.exit(1)

if __name__ == "__main__":
    main()