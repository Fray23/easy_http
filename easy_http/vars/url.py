from .base import BaseParserDecorator


class UrlVarsDecorator(BaseParserDecorator):
    def get_url(self):
        url = self.parser.get_url()
        url = self.set_vars(url)
        return url

    def set_vars(self, value):
        vars = self.get_vars_from_config()
        for k,v in vars.items():
            if type(v) is str:
                value = value.replace(k, v)
        return value
