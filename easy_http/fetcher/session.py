from abc import ABC, abstractmethod
import os
import pickle


class AbstractRequestSession(ABC):
    @abstractmethod
    def get_current_cookies(self):
        pass

    @abstractmethod
    def save_or_update_cookies(self):
        pass

    @abstractmethod
    def load_cookie(self):
        pass


class RequestSession(AbstractRequestSession):
    def __init__(self, session_path: str, session_file_name: str):
        self._session_path = os.path.join(session_path, session_file_name)
        self.cookie = None

    def load_cookie(self):
        try:
            self._try_to_load_and_set_cookie()
        except FileNotFoundError:
            pass
        except EOFError:
            pass

    def _try_to_load_and_set_cookie(self):
        _session_path = os.path.join(self._session_path)
        with open(_session_path, 'rb') as f:
            self.cookie = pickle.load(f)

    def save_or_update_cookies(self, new_cookies):
        self.load_cookie()
        if not self.cookie:
            self.cookie = new_cookies

        for new_cookie in new_cookies:
            self.cookie.set_cookie(new_cookie)

        self._save_pickle_cookie()

    def _save_pickle_cookie(self):
        with open(self._session_path, 'wb') as f:
            pickle.dump(self.cookie, f)

    def get_current_cookies(self):
        self.load_cookie()
        return self.cookie
