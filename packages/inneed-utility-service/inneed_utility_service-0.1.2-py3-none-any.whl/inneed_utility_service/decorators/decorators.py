from functools import wraps
from fastapi import Request
from inneed_utility_service.error_utility.error_handler import ErrorHandler, AuthenticationError

def validate_token_header(expected_token: str):
    """
    Decorator to validate the Authorization header with a configurable token.
    Uses the latest error handling utility.
    """
    def decorator(func):
        @wraps(func)
        @ErrorHandler.handle_error("Error while check authorization") 
        async def wrapper(request: Request, *args, **kwargs):
            token = request.headers.get("Authorization")

            if not token or token != f"Bearer {expected_token}":
                raise AuthenticationError("Invalid or missing token")

            return await func(request, *args, **kwargs)

        return wrapper
    return decorator
