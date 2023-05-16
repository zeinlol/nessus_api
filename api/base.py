from abc import ABC

from api.core import NessusCoreAPI
from api.mixins.plugins import PluginsMixin
from api.mixins.scans import ScanMixin
from core.tools import timed_print


class NessusAPI(NessusCoreAPI,
                PluginsMixin,
                ScanMixin,
                ABC):

    def __init__(self, username: str, password: str, host: str, port: int, secure: bool):
        super().__init__(username=username, password=password, host=host, port=port, secure=secure)
        if self.test_connection():
           self.login()
        else:
            timed_print('Can not establish connection. Exit')
            exit(1)
