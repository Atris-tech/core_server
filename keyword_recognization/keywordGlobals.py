import json
import os

class KeywordGlobals:
    def getGlobals(self, key):
        module_dir = os.path.dirname(__file__)  # get current directory
        file_path = os.path.join(module_dir, 'globals.json')

        with open(file_path, 'r') as f:
            config = json.load(f)
        server = config["server"]

        if key == "server":
            return server