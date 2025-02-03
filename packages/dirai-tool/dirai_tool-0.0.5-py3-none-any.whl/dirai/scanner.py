# scanner.py
import os
import sys
import pathspec
import re
from pathlib import Path

from dirai.utils import is_binary, redact_sensitive_data

apiKey=""
class DirectoryScanner:
    def __init__(self, config):
        self.config = config # consider to validate config here or in cli.py
        self.visited_links = set()
        self.gitignore_spec = None
        self.base_dir = None

        # Compile exclude and include patterns
        self.exclude_spec = pathspec.PathSpec.from_lines('gitwildmatch', config.get('exclude', []))
        self.include_spec = pathspec.PathSpec.from_lines('gitwildmatch', config.get('include', []))

    def _load_gitignore_spec(self):
        if not self.config.get('use_gitignore', True):
            return pathspec.PathSpec([])

        spec = pathspec.PathSpec([])

        for custom_path in self.config.get('gitignore_paths', []):
            if Path(custom_path).exists():
                with open(custom_path, 'r') as f:
                    spec += pathspec.PathSpec.from_lines('gitwildmatch', f)

        try:
            for root, _, files in os.walk(self.base_dir): # type: ignore
                if '.gitignore' in files:
                    gitignore_path = Path(root) / '.gitignore'
                    with open(gitignore_path, 'r') as f:
                        rel_path = Path(root).relative_to(self.base_dir) # type: ignore
                        lines = [
                            f"{rel_path}/{line.strip()}" if rel_path != Path('.') else line.strip()
                            for line in f if line.strip() and not line.startswith('#')
                        ]
                        spec += pathspec.PathSpec.from_lines('gitwildmatch', lines)
        except Exception as e:
            if self.config.get('verbose'):
                print(f"Gitignore error: {str(e)}", file=sys.stderr)

        return spec

    def _is_excluded(self, rel_path):
        abs_path = self.base_dir / rel_path
        is_dir = abs_path.is_dir()
        path_str = str(rel_path)

        if is_dir:
            path_str += '/'

        vcs_dirs = ['.git', '.svn', '.hg']
        if not self.config.get('include_vcs', False) and any(part in vcs_dirs for part in path_str.split(os.sep)):
            return True

        if self.exclude_spec.match_file(path_str):
            return True

        if self.gitignore_spec and self.gitignore_spec.match_file(path_str):
            return True

        if self.include_spec and not self.include_spec.match_file(path_str):
            if not is_dir:
                return True

        return False


    def _format_entry(self, name, is_dir=False, is_link=False, target=None):
        if is_link:
            return f"{name}@ -> {target}"
        if is_dir:
            return f"{name}/"
        return name

    def generate_structure(self, directory):
        self.base_dir = Path(directory).resolve()
        self.gitignore_spec = self._load_gitignore_spec()

        structure = [f"└── {self.base_dir.name}/"]
        structure += self._process_directory(self.base_dir)
        return structure

    def _process_directory(self, current_dir, prefix='', depth=0):
        structure = []
        max_depth = self.config.get('max_depth')
        if max_depth and depth > max_depth:
            return structure

        try:
            items = sorted(os.listdir(current_dir),
                         key=lambda x: (not os.path.isdir(os.path.join(current_dir, x)), x))
        except (PermissionError, FileNotFoundError):
            return [f"{prefix}└── [Permission denied]"]
        except Exception as e:
            return [f"{prefix}└── [Error: {str(e)}]"]

        for index, item in enumerate(items):
            path = current_dir / item
            is_last = index == len(items) - 1
            rel_path = path.relative_to(self.base_dir)

            if self._is_excluded(rel_path):
                continue

            is_link = path.is_symlink()
            target = None
            if is_link:
                try:
                    target = os.readlink(path)
                except Exception as e:
                    target = f"[Error: {str(e)}]"

            entry_line = self._format_entry(
                name=item,
                is_dir=path.is_dir() and not is_link,
                is_link=is_link,
                target=target
            )

            connector = "└── " if is_last else "├── "
            structure_line = f"{prefix}{connector}{entry_line}"
            structure.append(structure_line)

            if path.is_dir() and (not is_link or self.config.get('follow_symlinks')):
                if is_link and path in self.visited_links:
                    structure.append(f"{prefix}{'    ' if is_last else '│   '}│   [Recursive symlink skipped]")
                    continue
                if is_link:
                    self.visited_links.add(path)

                new_prefix = prefix + ('    ' if is_last else '│   ')
                structure += self._process_directory(
                    path,
                    prefix=new_prefix,
                    depth=depth + 1
                )

            elif self.config.get('show_content') and path.is_file() and not is_link:
                structure += self._show_file_content(path, prefix, is_last)

        return structure


    def _show_file_content(self, file_path, prefix, is_last):
        content_lines = []
        content_prefix = prefix + ('    ' if is_last else '│   ')
        max_lines = self.config.get('max_lines', 50)
        infinite_mode = max_lines == -1

        try:
            if is_binary(file_path):
                content_lines.append(f"{content_prefix}│   [Binary content omitted]")
                return content_lines

            with open(file_path, 'r', encoding='utf-8') as f:
                for line_num, line in enumerate(f):
                    # Handle infinite lines if max_lines is -1
                    if not infinite_mode and line_num >= max_lines:
                        content_lines.append(f"{content_prefix}│   [... {max_lines} lines shown]")
                        break

                    # Redact sensitive data before adding to output
                    cleaned_line = redact_sensitive_data(line.rstrip(), self.config.get('ignore_variables', []), self.config.get('redaction_patterns', []))
                    content_lines.append(f"{content_prefix}│   {cleaned_line}")

                    # Safety limit
                    if infinite_mode and line_num > 1000000:
                        content_lines.append(f"{content_prefix}│   [Stopped after 1,000,000 lines]")
                        break
        except Exception as e:
            content_lines.append(f"{content_prefix}│   [Error reading file: {str(e)}]")

        return content_lines