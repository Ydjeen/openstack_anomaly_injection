import json
from jsonschema import Draft7Validator
from jsonschema.exceptions import ValidationError
from os.path import abspath, join, curdir
import os.path


class CloudConfigParser:
    """Parser for validating and parsing the parameters for cloud configuration"""

    def __init__(self):
        path = os.path.abspath(__file__)
        dir_path = os.path.dirname(path)
        self.validator = Draft7Validator(json.load(open(join(dir_path, "schema.json"))))

    def _validate(self, config):
        self.validator.validate(config)

    def parse(self, config):
        self._validate(config)
        if isinstance(config, dict):
            return config
        else:
            return json.loads(config)
