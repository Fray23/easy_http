import re
from abc import ABC, abstractmethod


class AbstractParser(ABC):
    def __init__(self, path_to_request_file, path_to_project_dir):
        self.path_to_request_file = path_to_request_file
        self.path_to_project_dir = path_to_project_dir
        self.list_file_lines = self._load_file()

    def _load_file(self):
        lines = []
        with open(self.path_to_request_file) as request_file:
            for line in request_file.readlines():
                line = line.strip()
                if line.startswith('#'):
                    # Skipping comments
                    continue
                lines.append(line)
        return lines

    @abstractmethod
    def get_body_as_dict(self):
        pass

    @abstractmethod
    def get_url(self):
        pass


class AbstractHTTPParser(AbstractParser):
    def get_url(self):
        url_pattern = r"https?://.*"
        first_line = self.list_file_lines[0]

        match = re.search(url_pattern, first_line)

        if not match:
            raise Exception("no url")

        return match.group()

    def get_method(self):
        method_pattern = r"(POST|GET|PUT|PATCH)"
        match = re.search(method_pattern, self.list_file_lines[0], re.IGNORECASE)

        if not match:
            raise Exception("no method")

        return match.group().upper()

    def get_headers_as_dict(self):
        if self._file_text_has_only_url() or not self._file_text_has_header():
            return {}

        headers = self._extract_headers()
        return headers

    def _file_text_has_only_url(self) -> bool:
        return len(self.list_file_lines) < 2

    def _file_text_has_header(self) -> bool:
        if self._file_text_has_only_url():
            return False

        header_starter_line = self.list_file_lines[1]
        if header_starter_line.startswith('{'):
            return False
        return True

    def _extract_headers(self) -> dict:
        file_lines = self.list_file_lines
        headers = {}
        for line in file_lines[1:]:
            if line.startswith('{'):
                break
            if ': ' in line:
                name, value = line.split(': ', 1)
                headers[name] = value
        return headers
