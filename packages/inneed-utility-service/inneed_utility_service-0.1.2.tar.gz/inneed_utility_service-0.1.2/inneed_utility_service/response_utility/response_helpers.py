from fastapi import HTTPException
from inneed_utility_service.enums.enums import ResponseType
from typing import Any, Dict


def generate_error_response(error_type: ResponseType, details: str) -> HTTPException:
    """
    Generate a generic error response with an error type and corresponding status code.

    Args:
        error_type (ResponseType): The enumerated error type with its status code.
        details (str): A detailed error message.

    Returns:
        HTTPException: A FastAPI HTTPException object with the provided details.
    """
    return HTTPException(
        status_code=error_type.status_code,
        detail={
            "error_type": error_type.error_type,
            "error_message": details
        }
    )


def generate_success_response(message: str, data: Any = None) -> Dict[str, Any]:
    """
    Generate a success response with a message and optional data.

    Args:
        message (str): A success message.
        data (Any, optional): Additional data to include in the response. Defaults to None.

    Returns:
        dict: A dictionary containing the success message and optional data.
    """
    response = {"status": "success", "message": message}
    if data is not None:
        response["data"] = data
    return response
