from werkzeug.exceptions import HTTPException
from flask import make_response
import json


class FoundError(HTTPException):
    def __init__(self, status_code, message=''):
        self.response = make_response(message, status_code)


class NotGivenError(HTTPException):
    def __init__(self, status_code, error_code, error_message):
        message = {"error_code": error_code, "error_message": error_message}
        # return JSON string to keep consistent payload
        self.response = make_response(json.dumps(message), status_code)