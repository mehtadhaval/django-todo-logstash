import uuid


class RequestIdMiddleware(object):
    """
    Assigns a unique ID to every request
    """
    def __init__(self, get_response=None):
        self.get_response = get_response

    def __call__(self, request):
        response = None
        if hasattr(self, 'process_request'):
            response = self.process_request(request)
        if not response:
            response = self.get_response(request)
        if hasattr(self, 'process_response'):
            response = self.process_response(request, response)
        return response

    def process_request(self, request):
        request.request_id = self.generate_request_id()

    def generate_request_id(self):
        return uuid.uuid4().hex  # to avoid hyphens ("-") in the generated id

    def process_response(self, request, response):
        if hasattr(request, "request_id"):
            response['X-Request-Id'] = request.request_id
        return response
