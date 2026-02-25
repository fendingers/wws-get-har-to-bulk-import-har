"""
Shared XML utilities and configuration loader.
"""

import yaml

def get_settings():
    with open("config/settings.yaml", "r") as f:
        return yaml.safe_load(f)
