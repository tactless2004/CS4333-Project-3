'''
requests.py
CS4333 Project 3
Leyton McKinney
'''
import os
from util import HTTPRequest, HTTPResponse

def parse_request(request: str) -> HTTPRequest:
    '''
    Converts an HTTP request string into a `http_request.HTTPRequest` object
    
    :param request: Raw HTTP request string (utf-8 encoded)
    '''

    # Gather all fields, if packet is malformed, return an empty HTTPRequest
    #     generate_response() handles empty HTTPRequests as 400s
    try:
        fields = request.split('\n')
        request_type, request_target, http_version = fields[0].split(' ')
    except ValueError:
        return HTTPRequest("", "", "", "")

    # Default GET response should be image_test.html
    # Could consider making it index.html for ubiquity.
    if request_target == "/":
        request_target = "/image_test.html"

    # Gather all fields. Most will be unused
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


def _find_first_occurence(x: str, target: str) -> int:
    '''Returns the index of string `x` associated with the first occurance
    occurence of char `target`. Returns -1 if `target` is not found in `x`. O(n) search.
    '''
    for i, char in enumerate(x):
        if char == target:
            return i
    return -1

def generate_response(request: HTTPRequest) -> bytes:
    '''
    Generates an HTTP/1.1 compliant response for GET and HEAD requests.

    :param request: util.http_request.HTTPRequest object
    '''
    # TODO: Implement HEAD requests
    # Catch all non-get requests
    if not request.request_type in ["GET", "HEAD"]:
        return HTTPResponse(501).get()

    # Reroute external request_target path to correct internal path
    request.request_target = _fix_file_path(request.request_target)

    # If requested resource DNE, 404.
    if request.request_target == "":
        return HTTPResponse(404).get()

    # Handles edge case where HTTP Request is so mangled that the fields
    # cannot be adequately parsed.
    if request.request_type == "" and request.request_target == "":
        return HTTPResponse(400).get()

    # First assume request is successful.
    # If the resource is not found: 404, or the request is malformed: 400
    # then set_message() handles this.
    # Finally, get the bytes and return this response
    response = HTTPResponse(200)
    response.set_message(request.request_target)


    print(f"{response.status_code} " +
           f"\"{request.request_type} {request.request_target}\" {request.http_version}"
    )
    if request.request_type == "GET":
        return response.get()
    return response.head()

def _fix_file_path(path: str):
    if "/" in path:
        path = path.split("/")[-1]
    for directory, _, files in os.walk("local_html", topdown = True):
        for file in files:
            if path == file:
                return f"{directory.rstrip("\\")}/{file}"
    return ""
