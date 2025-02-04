# tests/test_utils.py
import pytest
from pathlib import Path
from dirai.utils import is_binary, redact_sensitive_data, validate_config, normalize_path

def test_is_binary_true(tmp_path):
    binary_file = tmp_path / "binary_file"
    binary_file.write_bytes(b'\x07\x08\x00\x09')
    assert is_binary(binary_file) is True

def test_is_binary_false(tmp_path):
    text_file = tmp_path / "text_file"
    text_file.write_text("This is a text file.")
    assert is_binary(text_file) is False

def test_redact_sensitive_data_ignore_vars(tmp_path):
    line = "DATABASE_URL=postgres://user:password@host:5432/database"
    redacted = redact_sensitive_data(line, ['DATABASE_URL'], [])
    assert redacted == "DATABASE_URL="

def test_redact_sensitive_data_redaction_patterns(tmp_path):
    line = "API_KEY=secret_value"
    redacted = redact_sensitive_data(line, [], ['API_KEY'])
    assert redacted == "API_KEY="

def test_validate_config_missing_key():
    with pytest.raises(ValueError, match="Missing required config key: exclude"):
        validate_config({'default': {'output': 'out.txt'}})

def test_validate_config_negative_max_depth():
    with pytest.raises(ValueError, match="max_depth cannot be negative"):
        validate_config({'default': {'exclude': [], 'output': 'out.txt', 'max_depth': -1}})

def test_validate_config_valid_max_depth():
    validate_config({'default': {'exclude': [], 'output': 'out.txt', 'max_depth': 0}})
    validate_config({'default': {'exclude': [], 'output': 'out.txt', 'max_depth': 1}})
    validate_config({'default': {'exclude': [], 'output': 'out.txt', 'max_depth': None}})


def test_normalize_path(tmp_path):
    test_path = tmp_path / "test_dir/../test_file.txt"
    normalized = normalize_path(test_path)
    assert normalized == tmp_path / "test_file.txt"