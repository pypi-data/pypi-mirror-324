# tests/test_scanner.py
import pytest
from pathlib import Path
from unittest.mock import patch, mock_open
from dirai.scanner import DirectoryScanner
from dirai.utils import is_binary
import os

@pytest.fixture
def scanner_instance():
    config = {
        'exclude': [],
        'include': [],
        'use_gitignore': False,
        'show_content': False,
        'max_depth': None,
        'follow_symlinks': False,
        'gitignore_paths': [],
        'verbose': False,
        'max_lines': -1,
    }
    return DirectoryScanner(config)



def test_load_gitignore_spec_custom(scanner_instance, tmp_path):
    gitignore_file = tmp_path / ".custom_gitignore"
    gitignore_file.write_text("*.log\n")
    scanner_instance.config['use_gitignore'] = True
    scanner_instance.config['gitignore_paths'] = [str(gitignore_file)]
    scanner_instance.base_dir = tmp_path
    spec = scanner_instance._load_gitignore_spec()
    assert any(p.pattern.startswith('*.log') for p in spec.patterns), f"Patterns found: {[p.pattern for p in spec.patterns]}"

def test_is_excluded_vcs(scanner_instance, tmp_path):
    scanner_instance.base_dir = tmp_path
    assert scanner_instance._is_excluded(Path('.git/')) is True
    scanner_instance.config['include_vcs'] = True
    assert scanner_instance._is_excluded(Path('.git/')) is False

def test_is_excluded_exclude_spec(scanner_instance, tmp_path):
    scanner_instance.base_dir = tmp_path
    scanner_instance.exclude_spec = scanner_instance.exclude_spec.from_lines('gitwildmatch', ['*.log'])
    assert scanner_instance._is_excluded(Path('test.log')) is True
    assert scanner_instance._is_excluded(Path('test.txt')) is False

def test_is_excluded_include_spec(scanner_instance, tmp_path):
    scanner_instance.base_dir = tmp_path
    scanner_instance.include_spec = scanner_instance.include_spec.from_lines('gitwildmatch', ['*.py'])
    assert scanner_instance._is_excluded(Path('test.log')) is True
    assert scanner_instance._is_excluded(Path('test.py')) is False



def test_process_directory_permission_error(scanner_instance, tmp_path):
    (tmp_path / 'inaccessible_dir').mkdir()
    # Simulate a permission error
    with patch('os.listdir', side_effect=PermissionError):
        result = scanner_instance._process_directory(tmp_path)
        assert result == ["└── [Permission denied]"]

def test_show_file_content_binary(scanner_instance, tmp_path):
    binary_file = tmp_path / 'binary.bin'
    binary_file.write_bytes(b'\x00\x01\x02')  # Write some binary data
    content = scanner_instance._show_file_content(binary_file, '', True)
    assert content == ["    │   [Binary content omitted]"]

def test_show_file_content_text(scanner_instance, tmp_path):
    text_file = tmp_path / 'text.txt'
    text_file.write_text('Hello\nWorld\n')
    content = scanner_instance._show_file_content(text_file, '', True)
    assert content == ["    │   Hello", "    │   World"]

def test_show_file_content_redaction(scanner_instance, tmp_path):
    text_file = tmp_path / 'sensitive.txt'
    text_file.write_text('API_KEY=secret_value')
    scanner_instance.config['redaction_patterns'] = ['API_KEY']
    content = scanner_instance._show_file_content(text_file, '', True) # type: ignore
    assert content == ["    │   API_KEY="]

def test_generate_structure_sort_order(scanner_instance, tmp_path):
    # Create files and directories in a specific order to test sorting
    (tmp_path / 'zzz_file.txt').touch()
    (tmp_path / 'aaa_dir').mkdir()
    (tmp_path / 'aaa_dir' / 'file_in_dir.txt').touch()
    (tmp_path / 'bbb_file.txt').touch()

    scanner_instance.base_dir = tmp_path
    structure = scanner_instance.generate_structure(tmp_path)

    expected_structure = [
        f"└── {tmp_path.name}/",
        "├── aaa_dir/",
        "│   └── file_in_dir.txt",
        "├── bbb_file.txt",
        "└── zzz_file.txt",
    ]
    assert structure == expected_structure, f"Expected structure:\n{expected_structure}\n\nGot:\n{structure}"