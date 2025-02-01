#!/usr/bin/env python3

"""mg - MultiGit - utility for managing multiple Git repos in a hierarchical directory tree"""

import os
import sys
import argparse
import fnmatch
import configparser

# TODO: Switch to tomlkit 
from collections import defaultdict

import thingy.git2 as git
import thingy.colour as colour

################################################################################

"""Configuration file format:

    [default]
    # Default settings

    [repo_path]
    name = path
    default branch = name
"""

# TODO: -j option to run in parallel?
# TODO: init function
# TODO: Use the configuration file
# TODO: Don't use a fixed list of default branch names
# TODO: / Output name of each git repo as it is processed as command sits there seeming to do nothing otherwise.
# TODO: ? Pull/fetch - only output after running command and only if something updated

################################################################################

DEFAULT_CONFIG_FILE = 'multigit.toml'

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

def find_git_repos(directory, wildcard):
    """Locate and return a list of '.git' directory parent directories in the
       specified path.
       If wildcard is not None then it is treated as a list of wildcards and
       only repos matching at least one of the wildcards are returned."""

    for root, dirs, _ in os.walk(directory):
        if '.git' in dirs:
            if root.startswith('./'):
                root = root[2:]

            if wildcard:
                for card in wildcard:
                    if fnmatch.fnmatch(root, card):
                        yield root
                        break
            else:
                yield root

################################################################################

def mg_init(args, config, console):
    """Create or update the configuration
       By default, it scans the tree for git directories and adds or updates them
       in the configuration, using the current branch as the default branch. """

    # Search for .git directories

    for repo in find_git_repos(args.directory, args.repos):
        if not args.quiet:
            show_progress(console.columns, repo)

        config[repo] = {'default branch': git.branch(path=repo)}

################################################################################

def mg_status(args, config, console):
    """Report Git status for any repo that has a non-empty status"""

    for repo in find_git_repos(args.directory, args.repos):
        if not args.quiet:
            show_progress(console.columns, repo)

        status = git.status(path=repo)
        branch = git.branch(path=repo)

        if status or branch != config[repo]['default branch']:
            if branch == config[repo]['default branch']:
                colour.write(f'[BOLD:{repo}]')
            else:
                colour.write(f'[BOLD:{repo}] - branch: [BLUE:{branch}]')

            staged = defaultdict(list)
            unstaged = defaultdict(list)
            untracked = []

            for entry in status:
                if entry[0] == '??':
                    untracked.append(entry[1])
                elif entry[0][0] == 'M':
                    staged['Updated'].append(entry[1])
                elif entry[0][0] == 'T':
                    staged['Type changed'].append(entry[1])
                elif entry[0][0] == 'A':
                    staged['Added'].append(entry[1])
                elif entry[0][0] == 'D':
                    staged['Deleted'].append(entry[1])
                elif entry[0][0] == 'R':
                    staged['Renamed'].append(entry[1])
                elif entry[0][0] == 'C':
                    staged['Copied'].append(entry[1])
                elif entry[0][1] == 'M':
                    colour.write(f'    WT Updated:      [BLUE:{entry[1]}]')
                elif entry[0][1] == 'T':
                    colour.write(f'    WT Type changed: [BLUE:{entry[1]}]')
                elif entry[0][1] == 'D':
                    unstaged['Deleted'].append(entry[1])
                elif entry[0][1] == 'R':
                    colour.write(f'    WT Renamed:      [BLUE:{entry[1]}]')
                elif entry[0][1] == 'C':
                    colour.write(f'    WT Copied:       [BLUE:{entry[1]}]')
                else:
                    staged['Other'].append(f'    {entry[0]}:    [BLUE:{entry[1]}]')

            if untracked:
                colour.write()
                colour.write('Untracked files:')

                for git_object in untracked:
                    colour.write(f'    [BLUE:{git_object}]')

            if staged:
                colour.write()
                colour.write('Changes staged for commit:')

                for item in staged:
                    for git_object in staged[item]:
                        colour.write(f'    {item}: [BLUE:{git_object}]')

            if unstaged:
                colour.write()
                colour.write('Changes not staged for commit:')

                for item in unstaged:
                    for git_object in unstaged[item]:
                        colour.write(f'    {item}: [BLUE:{git_object}]')

            colour.write()

################################################################################

def mg_fetch(args, config, console):
    """Run git fetch everywhere"""

    for repo in find_git_repos(args.directory, args.repos):
        if not args.quiet:
            show_progress(console.columns, repo)

        colour.write(f'Fetching updates for [BLUE:{repo}]')

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

    for repo in find_git_repos(args.directory, args.repos):
        if not args.quiet:
            show_progress(console.columns, repo)

        colour.write(f'Pulling updates for [BLUE:{repo}]')

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

################################################################################

def mg_checkout(args, config, console):
    """Run git checkout everywhere.
       By default it just checks out the specified branch (or the default branch)
       if the branch exists in the repo.
       If the 'create' option is specified then branch is created"""

    # TODO: Add --create handling

    for repo in find_git_repos(args.directory, args.repos):
        if not args.quiet:
            show_progress(console.columns, repo)

        branch = args.branch or config[repo]['default branch']

        if git.branch(path=repo) != branch:
            console.write(f'Checking out [BLUE:{branch}] in [BLUE:{repo}]')

            git.checkout(branch, path=repo)

################################################################################

def main():
    """Main function"""

    commands = {
       'init': mg_init,
       'status': mg_status,
       'fetch': mg_fetch,
       'pull': mg_pull,
       'push': mg_push,
       'checkout':  mg_checkout,
    }

    # Parse args in the form COMMAND OPTIONS SUBCOMMAND SUBCOMMAND_OPTIONS PARAMETERS

    parser = argparse.ArgumentParser(description='Gitlab commands')

    parser.add_argument('--dryrun', '--dry-run', '-D', action='store_true', help='Dry-run comands')
    parser.add_argument('--debug', '-d', action='store_true', help='Debug')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbosity to the maximum')
    parser.add_argument('--quiet', '-q', action='store_true', help='Minimal console output')
    parser.add_argument('--config', '-c', action='store', default=DEFAULT_CONFIG_FILE, help=f'The configuration file (defaults to {DEFAULT_CONFIG_FILE})')
    parser.add_argument('--directory', '--dir', action='store', default='.', help='The top-level directory of the multigit tree (defaults to the current directory)')
    parser.add_argument('--repos', '-r', action='append', default=None, help='The list of repo names to work on (defaults to all repos and can contain shell wildcards)')

    subparsers = parser.add_subparsers(dest='command')

    # Subcommands - currently just init, status, fetch, pull, push, with more to come

    parser_init = subparsers.add_parser('init', help='Build or update the configuration file using the current branch in each repo as the default branch')

    parser_status = subparsers.add_parser('status', help='Report git status in every repo that has something to report')
    parser_fetch = subparsers.add_parser('fetch', help='Run git fetch in every repo')
    parser_pull = subparsers.add_parser('pull', help='Run git pull in every repo')
    parser_push = subparsers.add_parser('push', help='Run git push in every repo where the current branch isn\'t the default and the most recent commit was by the current user')

    parser_checkout = subparsers.add_parser('checkout', help='Checkout the specified branch')
    parser_checkout.add_argument('--create', action='store_true', help='Create the specified branch and check it out')
    parser_checkout.add_argument('branch', nargs='?', default=None, action='store', help='The branch name to check out (defaults to the default branch)')

    # Parse the command line

    args = parser.parse_args()

    # Basic error checking

    if not args.command:
        error('No command specified')

    # TODO: If the config file isn't in the current directory then search up the directory tree for it but run in the current directory

    # If the configuration file exists, read it

    config = configparser.ConfigParser()

    if os.path.isfile(args.config):
        config.read(args.config)

    # Get the console size

    console = os.get_terminal_size()

    # Run the subcommand

    commands[args.command](args, config, console)

    # Save the updated configuration file

    if config:
        with open(args.config, 'w') as configfile:
            config.write(configfile)

################################################################################

def multigit():
    """Entry point"""

    try:
        main()
    except KeyboardInterrupt:
        sys.exit(1)
    except BrokenPipeError:
        sys.exit(2)

################################################################################

if __name__ == '__main__':
    multigit()
