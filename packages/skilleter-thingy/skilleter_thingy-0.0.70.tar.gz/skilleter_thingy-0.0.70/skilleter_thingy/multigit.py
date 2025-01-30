#!/usr/bin/env python3

"""mg - MultiGit - utility for managing multiple Git repos in a hierarchical directory tree"""

import os
import sys
import argparse

import tomlkit

import thingy.git2 as git
import thingy.colour as colour

################################################################################

"""Configuration file format:

    [default]
    # Default settings
    default branch = name

    [repos]
    name = path
    default branch = name

    [git-repo-location] # Either absolute or relative to the directory where the configuration file is found
    # Repo-specific settings to override default section
"""

# TODO: -j option to run in parallel
# TODO: init function
# TODO: Use the configuration file
# TODO: Don't use a fixed list of default branch names
# TODO: Output name of each git repo as it is processed as command sits there seeming to do nothing otherwise.

################################################################################

DEFAULT_CONFIG_FILE = 'multigit.toml'

DEFAULT_BRANCHES = ('main', 'scv-poc', 'master')

################################################################################

def error(msg, status=1):
    """Quit with an error"""

    sys.stderr.write(f'{msg}\n')
    sys.exit(status)

################################################################################

def show_progress(width, msg):
    """Show a single line progress message"""

    name = msg[:width-1]

    colour.write(f'{name}', newline=False)

    if len(name) < width-1:
        colour.write(' '*(width-len(name)), newline=False)

    colour.write('\r', newline=False)

################################################################################

def find_git_repos(directory):
    """Locate and return a list of '.git' directory parent directories in the
       specified path"""

    git_repos = []

    for root, dirs, _ in os.walk(directory):
        if '.git' in dirs:
            git_repos.append(root)

    return git_repos

################################################################################

def mg_init(args, config, console):
    """Create or update the configuration"""

    error('Not used - yet!')

    if config:
        print(f'Updating existing multigit configuration file - {args.config}')
        error('Not supported yet')
    else:
        print(f'Creating new multigit configuration file - {args.config}')

    # Search for .git directories

    git_repos = find_git_repos(args.directory)

################################################################################

def mg_status(args, config, console):
    """Report Git status for any repo that has a non-empty status"""

    for repo in find_git_repos(args.directory):
        if not args.quiet:
            show_progress(console.columns, repo)

        status = git.status(path=repo)
        branch = git.branch(path=repo)

        if status or branch not in DEFAULT_BRANCHES:
            if branch in DEFAULT_BRANCHES:
                colour.write(f'[BOLD:{repo}]')
            else:
                colour.write(f'[BOLD:{repo}] - branch: [BLUE:{branch}]')

            for entry in status:
                if entry[0] == '??':
                    colour.write(f'    Untracked: [BLUE:{entry[1]}]')
                else:
                    colour.write(f'    [BLUE:{entry}]')

            colour.write()

################################################################################

def mg_fetch(args, config, console):
    """Run git fetch everywhere"""

    for repo in find_git_repos(args.directory):
        if not args.quiet:
            show_progress(console.columns, repo)

        result = git.fetch(path=repo)

        if result:
            colour.write(f'[BOLD:{repo}]')
            for item in result:
                if item.startswith('From '):
                    colour.write(f'    [BLUE:{item}]')
                else:
                    colour.write(f'    {item}')

            colour.write()

################################################################################

def mg_pull(args, config, console):
    """Run git pull everywhere"""

    for repo in find_git_repos(args.directory):
        if not args.quiet:
            show_progress(console.columns, repo)

        try:
            result = git.pull(path=repo)
        except git.GitError as exc:
            error(f'Error in {repo}: {exc}')

        if result and result[0] != 'Already up-to-date.':
            colour.write(f'[BOLD:{repo}]')
            for item in result:
                if item.startswith('Updating'):
                    colour.write(f'    [BLUE:{item}]')
                else:
                    colour.write(f'    {item}')

            colour.write()

################################################################################

def mg_push(args, config, console):
    """Run git push everywhere where the current branch isn't one of the defaults
       and where the most recent commit was the current user and was on the branch
    """

    # TODO: Add option for force-push?
    # TODO: Add option for manual confirmation?

    pass

################################################################################

def main():
    """Main function"""

    commands = {
       'init': mg_init,
       'status': mg_status,
       'fetch': mg_fetch,
       'pull': mg_pull,
       'push': mg_push,
    }

    # Parse args in the form COMMAND OPTIONS SUBCOMMAND SUBCOMMAND_OPTIONS PARAMETERS

    parser = argparse.ArgumentParser(description='Gitlab commands')

    parser.add_argument('--dryrun', '--dry-run', '-D', action='store_true', help='Dry-run comands')
    parser.add_argument('--debug', '-d', action='store_true', help='Debug')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbosity to the maximum')
    parser.add_argument('--quiet', '-q', action='store_true', help='Minimal console output')
    parser.add_argument('--config', '-c', action='store', default=DEFAULT_CONFIG_FILE, help=f'The configuration file (defaults to {DEFAULT_CONFIG_FILE})')
    parser.add_argument('--directory', '--dir', action='store', default='.', help='The top-level directory of the multigit tree (defaults to the current directory)')

    subparsers = parser.add_subparsers(dest='command')

    # Subcommands - currently just init, status, fetch, pull, push, with more to come

    parser_init = subparsers.add_parser('init', help='')

    parser_status = subparsers.add_parser('status', help='Report git status in every repo that has one')
    parser_fetch = subparsers.add_parser('fetch', help='Run git fetch in every repo')
    parser_pull = subparsers.add_parser('pull', help='Run git pull in every repo')
    parser_push = subparsers.add_parser('push', help='Run git push in every repo where the current branch isn\'t the default and the most recent commit was by the current user')

    # Parse the command line

    args = parser.parse_args()

    # If the configuration file exists, read it

    config = tomlkit.loads(args.config) if os.path.isfile(args.config) else None

    # Get the console size

    console = os.get_terminal_size()

    # Run the subcommand

    commands[args.command](args, config, console)

################################################################################

def mg():
    """Entry point"""

    try:
        main()
    except KeyboardInterrupt:
        sys.exit(1)
    except BrokenPipeError:
        sys.exit(2)

################################################################################

if __name__ == '__main__':
    mg()
