import os
import json
from .base import BaseParserDecorator


class DefaultHeaderDecorator(BaseParserDecorator):
    def get_headers_as_dict(self):
        default_headrs = self._get_default_headrs()
        headers_from_parser = self.parser.get_headers_as_dict()
        if default_headrs is not None:
            headers_from_parser.update(default_headrs)
        return headers_from_parser

    def _get_default_headrs(self) -> dict:
        file_name = self._get_default_headr_file_name()
        if file_name is None:
            return None

        with open(file_name, 'r') as f:
            header_values = json.loads(f.read())
        return header_values

    def _get_default_headr_file_name(self) -> str:
        file_names = ['headers.json', 'header.json', 'h.json']
        finded_names = []
        for name in file_names:
            path_to_header_file = os.path.join(self.parser.path_to_project_dir, name)
            if os.path.exists(path_to_header_file):
                finded_names.append(path_to_header_file)

        if len(finded_names) > 1:
            raise Exception('Multiple header files found; please keep only one of them. Reserved names are headers.json, header.json, and h.json')
        if len(finded_names) == 0:
            return None
        return finded_names[0]
