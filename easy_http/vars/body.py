import uuid
import re
from .base import BaseParserDecorator


class BodyVarsDecorator(BaseParserDecorator):
    def get_body_as_dict(self):
        body = self.parser.get_body_as_dict()
        body = self.set_vars(body)
        return body

    def set_vars(self, _body):
        if isinstance(_body, dict):
            self._process_dict(_body)
        elif isinstance(_body, list):
            self._process_list(_body)
        return _body

    def _process_dict(self, body):
        for key, value in body.items():
            if isinstance(value, str):
                body[key] = self._replace_placeholders(value)
            elif isinstance(value, dict):
                self._process_dict(value)
            elif isinstance(value, list):
                self._process_list(value)

    def _process_list(self, items):
        for index, item in enumerate(items):
            if isinstance(item, dict):
                self._process_dict(item)
            elif isinstance(item, str):
                items[index] = self._replace_placeholders(item)

    def _replace_placeholders(self, value):
        value = value.replace('{{hex}}', uuid.uuid4().hex)
        value = value.replace('{{uuid}}', str(uuid.uuid4()))
        value = self._set_var_uuid_slice(value)
        value = self._set_custom_vars(value)
        return value

    @staticmethod
    def _set_var_uuid_slice(value):
        """
        Replaces {{uuid[N]}} in a string with the first N characters of a generated UUID.

        Example:
        Input: "User ID: {{uuid[8]}}, Session: {{uuid[16]}}"
        Output: "User ID: 123e4567, Session: 123e4567e89b12d3"
        """
        pattern = r'\{\{uuid\[(\d+)\]\}\}'

        def replace_uuid_slice(match):
            slice_length = int(match.group(1))
            return uuid.uuid4().hex[:slice_length]

        value = re.sub(pattern, replace_uuid_slice, value)
        return value

    def _set_custom_vars(self, value):
        vars = self.get_vars_from_config()
        for k,v in vars.items():
            if type(value) is str:
                if type(v) is not str:
                    if k in value:
                        value = v
                        break
                else:
                    value = value.replace(k, v)
        return value
