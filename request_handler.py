from http_request import http_request
def handle_get():
	assert http_request.REQUEST_TYPE == "GET"
	try: