'''
util/http_response.py
CS4333 Project 3
Leyton McKinney
'''
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
            # TODO: Add pdf support
            case "pdf":
                self.content_type = "application/pdf"
            case _:
                self.status_code = 400
                self.reason_phrase = code_reason_map[self.status_code]
