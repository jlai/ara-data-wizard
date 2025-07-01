import os.path
import tomllib

config = {}

for config_location in [".AraWizard.toml", os.path.expanduser("~/.AraWizard.toml")]:
    if os.path.exists(config_location):
        with open(config_location, "rb") as f:
            config = tomllib.load(f)

json_config = config.get("json", {})
