# tests/test_config.py
import pytest
from pathlib import Path
from unittest.mock import patch
from dirai.config import DiraiConfig
from dirai.constants import CONFIG_FILE_NAME, DEFAULT_CONFIG
import tempfile

@pytest.fixture
def config_instance():
    config = DiraiConfig()
    # Override the default config to match test expectations
    config.config_data = DEFAULT_CONFIG.copy()
    return config

def test_find_config_cwd(tmp_path, config_instance):
    config_file = tmp_path / CONFIG_FILE_NAME
    config_file.touch()
    with patch('pathlib.Path.cwd', return_value=tmp_path):
        assert config_instance._find_config() == config_file

# def test_find_config_home(tmp_path, config_instance):
#     config_file = tmp_path / CONFIG_FILE_NAME
#     config_file.touch()

#     # Create a dummy file in the directory two levels up from the test file
#     project_root = Path(__file__).parent.parent
#     dummy_config = project_root / CONFIG_FILE_NAME
#     dummy_config.touch()

#     def exists_side_effect(path, *args, **kwargs):
#         return str(path) == str(config_file) or str(path) == str(dummy_config)

#     # Patch paths to simulate config file found in home directory
#     with patch('pathlib.Path.home', return_value=tmp_path), \
#          patch('pathlib.Path.cwd', return_value=Path('nonexistent')), \
#          patch('pathlib.Path.exists', side_effect=exists_side_effect):
#         assert config_instance._find_config() == config_file

#     dummy_config.unlink()

def test_find_config_default(config_instance):
    with patch('pathlib.Path.cwd', return_value=Path('/nonexistent')), \
         patch('pathlib.Path.home', return_value=Path('/nonexistent')), \
         patch('pathlib.Path.exists', return_value=False):
        assert config_instance._find_config() is None

# def test_load_config_default(config_instance):
#     with patch.object(config_instance, '_find_config', return_value=None):
#         # Ensure the method returns the default configuration when no file is found
#         loaded_config = config_instance._load_config()

#         # Assert that the loaded config matches the updated DEFAULT_CONFIG
#         assert loaded_config == DEFAULT_CONFIG, f"Loaded config: {loaded_config}, Default config: {DEFAULT_CONFIG}"

def test_load_config_valid(tmp_path, config_instance):
    config_file = tmp_path / CONFIG_FILE_NAME
    config_file.write_text("web:\n  exclude: ['node_modules']\n")
    config_instance.config_path = config_file # directly set config path for testing

    # No need to rename default config file as we are mocking _find_config or directly setting config_path
    default_config_path = Path(__file__).parent.parent / CONFIG_FILE_NAME
    temp_file = None
    if default_config_path.exists():
        temp_file = default_config_path.with_suffix(".bak")
        default_config_path.rename(temp_file)

    with patch('pathlib.Path.cwd', return_value=tmp_path):
        config = config_instance._load_config() # this will now load from config_file path we set above
        assert 'web' in config, f"Loaded config keys: {config.keys()}"
        assert config['web']['exclude'] == ['node_modules']


    # Restore the original default config file
    if temp_file and temp_file.exists():
        temp_file.rename(default_config_path)

def test_merge_configs():
    base = {'default': {'a': 1, 'b': 2}, 'web': {'b': 3, 'c': 4}}
    user = {'web': {'c': 5, 'd': 6}, 'docs': {'e': 7}}
    merged = DiraiConfig()._merge_configs(base, user)
    assert merged == {
        'default': {'a': 1, 'b': 2},
        'web': {'b': 3, 'c': 5, 'd': 6},
        'docs': {'e': 7}
    }