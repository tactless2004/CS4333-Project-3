from http_request import HTTPRequest
def generate_response(request: HTTPRequest) -> bytes:
    '''
    Generates an HTTP/1.1 compliant response for GET and HEAD requests.

    :param request: http_request.HTTPRequest object
    '''
    # Catch all non-get requests
    if not request.request_type == "GET":
        return HTTPResponse(501).get()

    # Handles edge case where HTTP Request is so mangled that the fields
    # cannot be adequately parsed.
    if request.request_type == "" and request.request_target == "":
        return HTTPResponse(400).get()
    # First assume request is successful.
    # If the resource is not found: 404, or the request_type is malformed: 400
    # then set_message() handles this.
    # Finally, get the bytes and return this response
    response = HTTPResponse(200)
    response.set_message(request.request_target[1:])
    return response.get()

code_reason_map = {
    200 : "OK",
    400 : "Bad Request",
    404 : "Not Found",
    501 : "Not Implemented"
}
class HTTPResponse:
    '''HTTP Response object'''
    def __init__(self, status_code):
        self.status_code = status_code
        try:
            self.reason_phrase = code_reason_map[self.status_code]
        except ValueError:
            self.status_code = 400
            self.reason_phrase = code_reason_map[self.status_code]
        self.message_body = ""
        self.content_type = ""
        self.optional_headers = []
    def get(self) -> bytes:
        '''
        Returns a 'utf-8' encoded byte stream for the http response.
        '''
        if self.status_code in [400, 404, 501]:
            return f"HTTP/1.1 {self.status_code} {self.reason_phrase}\r\n".encode("utf-8")
        if self.content_type == "":
            raise ValueError("content type must be defined for a successful response.")
        if self.message_body == "":
            raise ValueError("message body must not be empty for a successful response.")

        match(self.content_type):
            case "text/html":
                return ("HTTP/1.1 200 OK\n" +
                    f"Content-Length: {len(self.message_body)}\n" +
                    f"Content-Type: {self.content_type}\n\n" +
                    "".join(self.optional_headers) +
                    f"{self.message_body}\n"
                ).encode("utf-8")

            case x if x in ["image/jpeg", "image/gif"]:
                return (("HTTP/1.1 200 OK\n" +
                f"Content-Length: {len(self.message_body)}\n" +
                f"Content-Type: {self.content_type}\n\n" +
                "".join(self.optional_headers)
                ).encode("utf-8") +
                self.message_body +
                "\r\n".encode("utf-8")
                )

    def set_message(self, fd: str):
        '''
        Setter for `self.content_type` and `self.message_body.
        '''
        try:
            extension = fd.split(".")[1]
        except IndexError:
            print("Invalid get request")
            self.status_code = 400
            self.reason_phrase = code_reason_map[self.status_code]
            return
        try:
            self.message_body = open(fd, "rb").read()
        except FileNotFoundError:
            print(f"Requested resource {fd} does not exist.")
            self.status_code = 404
            self.reason_phrase = code_reason_map[self.status_code]
            return

        match(extension):
            case "html":
                self.message_body = open(
                    file= fd,
                    mode = "r",
                    encoding = "utf-8"
                ).read()
                self.content_type = "text/html"
            case "gif":
                self.message_body = open(fd, "rb").read()
                self.content_type = "image/gif"
            case x if x in ["jpeg", "jpg"]:
                self.message_body = open(fd, "rb").read()
                self.content_type = "image/jpeg"
            case "pdf":
                self.content_type = "application/pdf"
            case _:
                self.status_code = 400
                self.reason_phrase = code_reason_map[self.status_code]
        
