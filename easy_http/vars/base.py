import os
import json
from parser import AbstractHTTPParser


class BaseParserDecorator:
    def __init__(self, parser: AbstractHTTPParser):
        self.parser = parser

    def __getattr__(self, name):
        return getattr(self.parser, name)

    def get_vars_from_config(self) -> dict:
        file_name = self._get_vars_file_name()
        if file_name is None:
            return None

        with open(file_name, 'r') as f:
            values = json.loads(f.read())
        return values

    def _get_vars_file_name(self) -> str:
        file_names = ['vars.json', 'var.json', 'v.json']
        finded_names = []
        for name in file_names:
            path_to_file = os.path.join(self.parser.path_to_project_dir, name)
            if os.path.exists(path_to_file):
                finded_names.append(path_to_file)

        if len(finded_names) > 1:
            raise Exception(
                'Multiple vars files found; please keep only one of them.' +
                'Reserved names are vars.json, var.json, and v.json'
            )
        if len(finded_names) == 0:
            return None
        return finded_names[0]
