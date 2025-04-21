# pylint disable=C0103
'''
util/http_request.py
CS4333 Project 3
Leyton McKinney
'''
from dataclasses import dataclass

@dataclass
class HTTPRequest:
    '''Dataclass representing a parsed http request. This class has no method members.'''
    request_type: str
    request_target: str
    http_version: float
    header: dict
