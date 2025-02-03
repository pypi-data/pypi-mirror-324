import sys
from pathlib import Path
import yaml
from dirai.constants import CONFIG_FILE_NAME, DEFAULT_CONFIG

class DiraiConfig:
    def __init__(self):
        self.config_path = self._find_config()
        self.config_data = self._load_config()

    def _find_config(self):
        search_paths = [
            Path.cwd(),
            Path.home(),
            Path(__file__).parent.parent
        ]
    
        for path in search_paths:
            config_file = path / CONFIG_FILE_NAME
            if config_file.exists():
                return config_file
        print("Config file not found. Using default configuration.")
        return None

    def _load_config(self):
        if not self.config_path:
            return DEFAULT_CONFIG
            
        try:
            with open(self.config_path, 'r') as f:
                user_config = yaml.safe_load(f) or {}
                return self._merge_configs(DEFAULT_CONFIG, user_config)
        except Exception as e:
            print(f"Error loading config: {e}", file=sys.stderr)
            return DEFAULT_CONFIG

    def _merge_configs(self, base, user):
        merged = base.copy()
        for profile, settings in user.items():
            if profile in merged:
                merged_profile = merged[profile].copy()
                for key, value in settings.items():
                    if isinstance(value, dict) and isinstance(merged_profile.get(key), dict):
                        merged_profile[key] = {**merged_profile[key], **value}
                    else:
                        merged_profile[key] = value
                merged[profile] = merged_profile
            else:
                merged[profile] = settings
        return merged

    def get_profile(self, profile_name):
        return self.config_data.get(profile_name, self.config_data["default"])
    # generate get_profile_names
    def get_profile_names(self):
        return list(self.config_data.keys())
    
    def get_profile_names_except_default(self):
        return [name for name in self.config_data.keys() if name != "default"]