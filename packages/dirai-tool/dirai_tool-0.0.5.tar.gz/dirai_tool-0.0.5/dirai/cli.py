#!/usr/bin/env python3
"""
DIRAI - Enhanced Directory Structure Analyzer (No Color Version)
"""

import argparse
import os
import sys
import platform
from pathlib import Path
import yaml
import pathspec

from dirai.scanner import DirectoryScanner
from dirai.config import DiraiConfig
from dirai.constants import CONFIG_FILE_NAME, DEFAULT_CONFIG
# Configuration Constants



def main():
    config_handler = DiraiConfig()
    args = parse_arguments(config_handler)
    if args.profiles and "all" in args.profiles:
        # Run all profiles from the config file
        profiles = config_handler.get_profile_names()
    else:
        profiles = args.profiles or [args.profile]

    for profile_name in profiles:
        run_profile(profile_name, config_handler, args)

def parse_arguments(config_handler):    
    parser = argparse.ArgumentParser(
        prog="dirai",
        description="DIRAI - Smart Directory Structure Analysis",
        epilog="Example: dirai --profile web --output structure.md\n"
               "Configuration file: ~/.dirai.yaml or current directory"
    )
    
    parser.add_argument("-p", "--profile", default="all",
                        help="Configuration profile to use")
    parser.add_argument("--profiles", nargs='+',default='all',
                        help="Run multiple profiles sequentially. Use 'all' to run all profiles from config")
    parser.add_argument("-d", "--directory", default=".",
                        help="Target directory to analyze")
    parser.add_argument("-o", "--output", 
                        help="Output file name")
    parser.add_argument("-x", "--exclude", nargs='+',
                        help="Exclusion patterns (supports gitignore syntax)")
    parser.add_argument("-i", "--include", nargs='+',
                        help="Inclusion patterns (supports gitignore syntax)")
    parser.add_argument("--max-depth", type=int,
                        help="Maximum directory depth")
    parser.add_argument("--use-gitignore", type=lambda x: x.lower() in ['true', 'yes', '1'],
                        help="Override gitignore usage (true/false)")
    parser.add_argument("--gitignore-paths", nargs='+',
                        help="Additional gitignore files to use")
    parser.add_argument("--show-content", action="store_const", const=True, default=None,
                        help="Display file contents")
    parser.add_argument("--follow-symlinks", action="store_const", const=True, default=None,
                        help="Follow symbolic links")
    parser.add_argument("--verbose", action="store_const", const=True, default=None,
                        help="Show detailed error messages")
    
    return parser.parse_args()

def run_profile(profile_name, config_handler, cli_args):
    base_config = config_handler.get_profile(profile_name)
    
    cli_args_dict = {k: v for k, v in vars(cli_args).items() if v is not None}
    
    config = {**base_config, **cli_args_dict}
    
    for list_field in ['exclude', 'include', 'gitignore_paths']:
        if list_field in cli_args_dict and list_field in base_config:
            config[list_field] = base_config[list_field] + cli_args_dict.get(list_field, [])
    
    scanner = DirectoryScanner(config)
    structure = scanner.generate_structure(config['directory'])
    
    output_file = config.get('output', 'project_structure.txt')
    with open(output_file, 'w', encoding='utf-8') as f:
        for line in structure:
            f.write(line + '\n')
    
    if config.get('output') != '-':
        print(f"DIRAI report generated: {output_file}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
        sys.exit(1)