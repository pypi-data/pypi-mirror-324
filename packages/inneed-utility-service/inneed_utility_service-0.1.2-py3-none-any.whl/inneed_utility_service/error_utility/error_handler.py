from typing import Optional, Type

class BaseUtilityError(Exception):
    """Base exception for all utility errors."""
    def __init__(self, message: str, original_exception: Optional[Exception] = None):
        super().__init__(message)
        self.original_exception = original_exception
        self.detail = {
            "error_type": self.__class__.__name__,
            "message": message,
            "original_exception": str(original_exception) if original_exception else None
        }
        
#Authentication errors
class AuthenticationError(BaseUtilityError):
    """Base class from auth related error"""

# S3-specific errors
class S3Error(BaseUtilityError):
    """Base class for S3-related errors."""

class S3ConnectionError(S3Error):
    """Error connecting to S3."""

class S3OperationError(S3Error):
    """Generic S3 operation failure."""

class S3ObjectNotFoundError(S3Error):
    """Requested object not found in S3."""

# Database-related errors
class DatabaseError(BaseUtilityError):
    """Base class for database errors."""

class DatabaseConnectionError(DatabaseError):
    """Failed to connect to database."""

class DatabaseQueryError(DatabaseError):
    """Error executing database query."""

class DatabaseTimeoutError(DatabaseError):
    """Database operation timed out."""
    
# DynamoDB-specific errors
class DynamoDBError(BaseUtilityError):
    """Base class for DynamoDB-related errors."""

class DynamoDBConnectionError(DynamoDBError):
    """Error connecting to DynamoDB."""

class DynamoDBOperationError(DynamoDBError):
    """Generic DynamoDB operation failure."""

# ORM-specific errors
class ORMError(BaseUtilityError):
    """Base class for ORM-related errors."""

class ORMSessionError(ORMError):
    """Database session management error."""

class ORMObjectNotFoundError(ORMError):
    """Requested object not found through ORM."""

class ORMValidationError(ORMError):
    """Data validation failed in ORM layer."""

# Cognito-specific errors
class CognitoError(BaseUtilityError):
    """Base class for Cognito-related errors."""

class CognitoConnectionError(CognitoError):
    """Error connecting to Cognito."""

class CognitoOperationError(CognitoError):
    """Generic Cognito operation failure."""

class CognitoUserNotFoundError(CognitoError):
    """Requested user not found in Cognito."""

# Generic error handler
class ErrorHandler:
    @staticmethod
    def handle_error(error: Type[BaseUtilityError], message: str, raise_exception: bool = True):
        """
        Generic error handling decorator.
        
        Args:
            error: The error class to be raised.
            message: A custom message to prefix the error.
            raise_exception: If True, the wrapped exception is raised.
            
        Returns:
            A decorator that wraps the function call in a try/except block.
        """
        def decorator(func):
            def wrapper(*args, **kwargs):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    err = error(
                        message=f"{message}: {str(e)}",
                        original_exception=e
                    )
                    if raise_exception:
                        raise err from e
                    return err
            return wrapper
        return decorator
