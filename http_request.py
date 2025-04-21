# pylint disable=C0103
'''http_request module'''
from dataclasses import dataclass

@dataclass
class http_request:
    '''Dataclass representing a parsed http request. This class has no method members.'''
    request_type: str
    request_target: str
    http_version: float
    header: dict
