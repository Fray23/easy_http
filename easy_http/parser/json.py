import json
from .abstract import AbstractHTTPParser


class HttpJsonParser(AbstractHTTPParser):
    def get_body_as_dict(self):
        body_txt = ""
        json_start = False
        lines = self.list_file_lines

        if self._file_text_has_only_url():
            return {}

        for line in lines:
            if json_start or ('{' in line or '[' in line):
                json_start = True
            else:
                continue
            body_txt += line

        if body_txt.strip():
            return json.loads(body_txt)
        return None
