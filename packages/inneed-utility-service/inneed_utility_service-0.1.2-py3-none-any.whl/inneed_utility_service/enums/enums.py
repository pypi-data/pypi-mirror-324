from enum import Enum

class ResponseType(Enum):
    # 2xx Success
    OK = ("OK", 200)
    CREATED = ("Created", 201)
    ACCEPTED = ("Accepted", 202)
    NO_CONTENT = ("NoContent", 204)

    # 4xx Client Errors
    VALIDATION_ERROR = ("ValidationError", 400)
    AUTHENTICATION_ERROR = ("AuthenticationError", 401)
    AUTHORIZATION_ERROR = ("AuthorizationError", 403)
    NOT_FOUND_ERROR = ("NotFoundError", 404)
    METHOD_NOT_ALLOWED = ("MethodNotAllowed", 405)
    CONFLICT_ERROR = ("ConflictError", 409)
    UNSUPPORTED_MEDIA_TYPE = ("UnsupportedMediaType", 415)
    UNPROCESSABLE_ENTITY = ("UnprocessableEntity", 422)
    TOO_MANY_REQUESTS = ("TooManyRequests", 429)

    # 5xx Server Errors
    INTERNAL_SERVER_ERROR = ("InternalServerError", 500)
    NOT_IMPLEMENTED = ("NotImplemented", 501)
    BAD_GATEWAY = ("BadGateway", 502)
    SERVICE_UNAVAILABLE = ("ServiceUnavailable", 503)
    GATEWAY_TIMEOUT = ("GatewayTimeout", 504)

    def __init__(self, error_type: str, status_code: int):
        self.error_type = error_type
        self.status_code = status_code

