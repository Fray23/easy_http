import uuid
import re
import os
import json
from .base import BaseParserDecorator


class BodyVarsDecorator(BaseParserDecorator):
    def get_body_as_dict(self):
        body = self.parser.get_body_as_dict()
        body = self.set_vars(body)
        return body

    @classmethod
    def set_vars(cls, _body):
        """Main method to process and replace placeholders in the input body."""
        if isinstance(_body, dict):
            cls._process_dict(_body)
        elif isinstance(_body, list):
            cls._process_list(_body)
        return _body

    @classmethod
    def _process_dict(cls, body):
        """Process each key-value pair in a dictionary."""
        for key, value in body.items():
            if isinstance(value, str):
                body[key] = cls._replace_placeholders(value)
            elif isinstance(value, dict):
                cls._process_dict(value)
            elif isinstance(value, list):
                cls._process_list(value)

    @classmethod
    def _process_list(cls, items):
        """Process each item in a list."""
        for index, item in enumerate(items):
            if isinstance(item, dict):
                cls._process_dict(item)
            elif isinstance(item, str):
                items[index] = cls._replace_placeholders(item)

    @classmethod
    def _replace_placeholders(cls, value):
        """Replace placeholders in a string with corresponding generated values."""

        value = value.replace('{{hex}}', uuid.uuid4().hex)
        value = value.replace('{{uuid}}', str(uuid.uuid4()))
        value = cls._set_var_uuid_slice(value)
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
