# dirai/cli.py
#!/usr/bin/env python3
"""
DIRAI - Enhanced Directory Structure Analyzer (No Color Version)
"""

import os
import sys
from pathlib import Path
import click
from dirai.scanner import DirectoryScanner
from dirai.config import DiraiConfig
from dirai.constants import CONFIG_FILE_NAME, DEFAULT_CONFIG
import pytest
from unittest.mock import patch, MagicMock
from dirai.cli import parse_arguments

@click.command()
@click.option("--profiles", default="default", help="Run multiple profiles sequentially. Use 'all' to run all profiles from config")
@click.option("-d", "--directory", default=".", help="Target directory to analyze")
@click.option("-o", "--output", help="Output file name")
@click.option("-x", "--exclude", multiple=True, help="Exclusion patterns (supports gitignore syntax)")
@click.option("-i", "--include", multiple=True, help="Inclusion patterns (supports gitignore syntax)")
@click.option("--max-depth", type=int, help="Maximum directory depth")
@click.option("--use-gitignore", is_flag=True, default=None, help="Override gitignore usage (true/false)")
@click.option("--gitignore-paths", multiple=True, help="Additional gitignore files to use")
@click.option("--show-content", is_flag=True, default=None, help="Display file contents")
@click.option("--follow-symlinks", is_flag=True, default=None, help="Follow symbolic links")
@click.option("--verbose", is_flag=True, default=None, help="Show detailed error messages")
def main(profiles, directory, output, exclude, include, max_depth, use_gitignore, gitignore_paths, show_content, follow_symlinks, verbose):
    """
    DIRAI - Smart Directory Structure Analysis

    Example: dirai --profiles web --output structure.md

    Configuration file: ~/.dirai.yaml or current directory
    """
    config_handler = DiraiConfig()

    # Determine which profiles to run
    if profiles:
        if "all" in profiles:
            profiles = config_handler.get_profile_names_except_default()
        else:
            profiles = profiles.split(",")
    else:
        profiles = ["default"]

    for profile_name in profiles:
        run_profile(profile_name, config_handler, directory, output, exclude, include, max_depth, use_gitignore, gitignore_paths, show_content, follow_symlinks, verbose)

def run_profile(profile_name, config_handler, directory, output, exclude, include, max_depth, use_gitignore, gitignore_paths, show_content, follow_symlinks, verbose):
    base_config = config_handler.get_profile(profile_name)

    # Convert tuple arguments to lists
    exclude_list = list(exclude)
    include_list = list(include)
    gitignore_paths_list = list(gitignore_paths)

    # Merge CLI arguments with the base configuration
    config = {
        **base_config,
        "directory": directory,
        "output": output,
        "exclude": exclude_list,
        "include": include_list,
        "max_depth": max_depth,
        "use_gitignore": use_gitignore,
        "gitignore_paths": gitignore_paths_list,
        "show_content": show_content,
        "follow_symlinks": follow_symlinks,
        "verbose": verbose
    }

    # Further merge or override settings from the CLI as needed
    for list_field in ['exclude', 'include', 'gitignore_paths']:
        if list_field in config and config[list_field]:
            config[list_field] = base_config.get(list_field, []) + config[list_field]

    scanner = DirectoryScanner(config)
    structure = scanner.generate_structure(config['directory'])

    output_file = config.get('output', 'project_structure.txt')
    with open(output_file, 'w', encoding='utf-8') as f:
        for line in structure:
            f.write(line + '\n')

    if config.get('output') != '-':
        print(f"DIRAI report generated: {output_file}")

@pytest.fixture
def mock_config_handler():
    config = DiraiConfig()
    config.get_profile = MagicMock(return_value={
        'exclude': [],
        'include': [],
        'use_gitignore': True,
        'show_content': True,
        'directory': '.',
        'output': 'structure.txt'
    })
    return config

def test_parse_arguments_defaults(mock_config_handler):
    with patch('sys.argv', ['dirai']):
        args = parse_arguments(mock_config_handler)
        assert args.profiles == 'all'
        assert args.directory == '.'
        assert args.output is None
        assert args.exclude is None
        assert args.include is None

def test_parse_arguments_custom(mock_config_handler):
    test_args = [
        'dirai',
        '--profiles', 'web', 'docs',
        '--directory', '/test/path',
        '--output', 'output.md',
        '--exclude', '*.log', '*.tmp',
        '--max-depth', '3'
    ]
    with patch('sys.argv', test_args):
        args = parse_arguments(mock_config_handler)
        assert args.profiles == ['web', 'docs']
        assert args.directory == '/test/path'
        assert args.output == 'output.md'
        assert args.exclude == ['*.log', '*.tmp']
        assert args.max_depth == 3

# def test_run_profile(mock_config_handler, tmp_path):
#     cli_args = MagicMock()
#     cli_args.directory = str(tmp_path)
#     cli_args.output = 'test_output.txt'
#     cli_args.exclude = ['*.tmp']
#     cli_args.include = None
#     cli_args.max_depth = None
#     cli_args.use_gitignore = None
#     cli_args.gitignore_paths = None
#     cli_args.show_content = None
#     cli_args.follow_symlinks = None
#     cli_args.verbose = None

#     # Create a test file
#     test_file = tmp_path / "test.txt"
#     test_file.write_text("test content")

#     with patch('dirai.cli.DirectoryScanner') as mock_scanner:
#         mock_scanner_instance = mock_scanner.return_value
#         mock_scanner_instance.generate_structure.return_value = ['└── test/']
        
#         run_profile('test_profile', mock_config_handler, cli_args)
        
#         # Verify scanner was called with merged config
#         mock_scanner.assert_called_once()
#         config_arg = mock_scanner.call_args[0][0]
#         assert config_arg['directory'] == str(tmp_path)
#         assert config_arg['output'] == 'test_output.txt'
#         assert '*.tmp' in config_arg['exclude']

# def test_run_profile_merge_lists(mock_config_handler):
#     # Test that list fields are properly merged between profile and CLI args
#     base_config = {
#         'exclude': ['*.pyc'],
#         'include': ['*.py'],
#         'gitignore_paths': ['.gitignore'],
#         'directory': '.',
#         'output': 'out.txt'
#     }
#     mock_config_handler.get_profile.return_value = base_config

#     cli_args = MagicMock()
#     cli_args.exclude = ['*.tmp']
#     cli_args.include = ['*.md']
#     cli_args.gitignore_paths = ['custom.gitignore']
#     cli_args.directory = '.'
#     cli_args.output = None
#     cli_args.max_depth = None
#     cli_args.use_gitignore = None
#     cli_args.show_content = None
#     cli_args.follow_symlinks = None
#     cli_args.verbose = None

#     with patch('dirai.cli.DirectoryScanner') as mock_scanner:
#         mock_scanner_instance = mock_scanner.return_value
#         mock_scanner_instance.generate_structure.return_value = ['└── test/']
        
#         run_profile('test_profile', mock_config_handler, cli_args)
        
#         config_arg = mock_scanner.call_args[0][0]
#         assert set(config_arg['exclude']) == {'*.pyc', '*.tmp'}
#         assert set(config_arg['include']) == {'*.py', '*.md'}
#         assert set(config_arg['gitignore_paths']) == {'.gitignore', 'custom.gitignore'}

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
        sys.exit(1)