# TODO: docstring
from http_request import HTTPRequest

def parse_http_request(request: str) -> HTTPRequest:
    '''TODO: Doctstring'''
    try:
        fields = request.split('\n')
        request_type, request_target, http_version = fields[0].split(' ')
    except ValueError:
        return HTTPRequest("", "", "", "")
    print(request_target)
    header = {}
    for field in fields[1:]:
        i = _find_first_occurence(field, ":")
        if i == -1:
            continue
        header_field, value = field[0:i], field[i+1:].lstrip().rstrip()
        header[header_field] = value

    return HTTPRequest(
        request_type,
        request_target,
        http_version,
        header
    )
    # TODO: Request_Type checking

def _find_first_occurence(x: str, target: str) -> int:
    '''Returns the index of `x` associated with the first occurance
    occurence of char `target`.
    '''
    for i, char in enumerate(x):
        if char == target:
            return i
    return -1
