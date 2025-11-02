from flask import jsonify

class NotGivenError(Exception):
    """Raised when required input is missing or invalid."""
    def __init__(self, status_code=400, error_code=None, error_message=None):
        self.status_code = status_code
        self.error_code = error_code
        self.error_message = error_message or "Required input not provided."
        super().__init__(self.error_message)


class FoundError(Exception):
    """Raised when a resource is not found or already exists."""
    def __init__(self, status_code=404, error_code=None, error_message=None):
        self.status_code = status_code
        self.error_code = error_code
        self.error_message = error_message or "Resource not found or already exists."
        super().__init__(self.error_message)


class ConflictError(Exception):
    """Raised when there is a conflict with an existing resource."""
    def __init__(self, status_code=409, error_code=None, error_message=None):
        self.status_code = status_code
        self.error_code = error_code
        self.error_message = error_message or "Conflict detected."
        super().__init__(self.error_message)


def handle_error(error, status_code=None):
    """Return standardized JSON error response."""
    status = getattr(error, "status_code", status_code or 500)
    message = getattr(error, "error_message", str(error))
    code = getattr(error, "error_code", "INTERNAL_ERROR")

    response = jsonify({
        "error_code": code,
        "error_message": message,
        "status": status
    })
    response.status_code = status
    return response
