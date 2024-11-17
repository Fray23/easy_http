from parser import AbstractHTTPParser


class BaseParserDecorator:
    def __init__(self, parser: AbstractHTTPParser):
        self.parser = parser

    def __getattr__(self, name):
        return getattr(self.parser, name)
