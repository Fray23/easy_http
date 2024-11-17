from dataclasses import dataclass
import requests
import json
from .session import AbstractRequestSession
from .enum import ContentTypeEnum


@dataclass
class RequestObj:
    url: str
    method: str
    headers: dict
    body: dict

    @property
    def content_type(self):
        content_type = None

        for key, val in self.headers.items():
            if key == ContentTypeEnum.key:
                content_type = val

        if content_type is None:
            content_type = ContentTypeEnum.default
        return content_type


class HttpFetcher():
    METHODS = {
        'POST': requests.post,
        'GET': requests.get,
        'PUT': requests.put,
        'PATCH': requests.patch
    }

    def __init__(self, session: AbstractRequestSession):
        self.cookie_session = session

    def send_with_save_session(self, request_obj: RequestObj):
        resp = self.send_request(request_obj)
        self._print_response(resp)
        self.save_or_update_cookies(resp.cookies)

    def send_request(self, request_obj: RequestObj):
        try:
            return self._try_to_send(request_obj)
        except Exception as e:
            print(f"Get Error when send request: {e}")

    def _try_to_send(self, request_obj: RequestObj):
        request_func = self.METHODS[request_obj.method]
        cookie = self.cookie_session.get_current_cookies()

        request_kwargs = dict(
            url=request_obj.url,
            headers=request_obj.headers,
            cookies=cookie,
        )
        if request_obj.method == 'GET':
            request_kwargs['params'] = request_obj.body
        elif request_obj.content_type == ContentTypeEnum.json:
            request_kwargs['json'] = request_obj.body
        else:
            request_kwargs['data'] = request_obj.body
        resp = request_func(**request_kwargs)
        return resp

    def _print_response(self, resp):
        print(f"// status_code {'':<18} {resp.status_code}")
        for header_name, header_value in resp.headers.items():
            print(f"// {header_name:<30} {header_value}")
        try:
            resp_content = resp.json()
            print(json.dumps(resp_content, indent=2))
        except ValueError:
            print(resp.content)

    def save_or_update_cookies(self, cookies):
        try:
            self.cookie_session.save_or_update_cookies(cookies)
        except Exception as e:
            print(f"Get Error when save or update cookies: {e}")
