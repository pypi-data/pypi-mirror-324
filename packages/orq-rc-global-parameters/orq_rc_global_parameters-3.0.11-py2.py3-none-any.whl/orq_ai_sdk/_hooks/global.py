import requests
from typing import Optional, Tuple, Union
from .types import BeforeRequestContext, BeforeRequestHook
from requests.structures import CaseInsensitiveDict
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse


class ExampleHook(BeforeRequestHook):
    def before_request(self, hook_ctx: BeforeRequestContext, request: requests.PreparedRequest) -> Union[requests.PreparedRequest, Exception]:

        return request