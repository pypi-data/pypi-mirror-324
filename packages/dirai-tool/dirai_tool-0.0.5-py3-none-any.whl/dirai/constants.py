CONFIG_FILE_NAME = ".dirai.yaml"
DEFAULT_CONFIG = {
    "default": {
        "exclude": [],
        "include": [],
        "use_gitignore": True,
        "show_content": True,
        "show_hidden": False,
        "output": "structure.txt",
        "max_depth": None,
        "follow_symlinks": False,
        "gitignore_paths": [],
        "max_lines": -1,
        "include_vcs": False,
        "ignore_variables": [],
        "redaction_patterns": [
            r'api[_-]?key',
            r'secret[_-]?key',
            r'token',
            r'password',
            r'credentials',
            r'auth',
            r'authorization',
            r'access',
            r'session',
            r'cookie',
            r'bearer',
            r'api_key',
            r'api_token',
            r'api_secret',
            r'api_password',
            r'api_username',
            r'apikey',
            r'apitoken',
            r'apisecret',
            r'apipassword',
            r'apiusername',
            
    
        ]
    }
}

