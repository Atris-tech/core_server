import json
import os

class Config:
    def getGlobals(self, key):
        module_dir = os.path.dirname(__file__)  # get current directory
        file_path = os.path.join(module_dir, 'uploads.json')
        with open(file_path, 'r') as f:
            config = json.load(f)
        container = config["container"]
        connection_str = config["connection_str"]
        allowed_types = config["allowed_types"]
        account_url = config["account_url"]

        if key == "container":
            return container
        elif key == "connection_str":
            return connection_str
        elif key == "allowed-types":
            return allowed_types
        elif key == "account_url":
            return account_url

