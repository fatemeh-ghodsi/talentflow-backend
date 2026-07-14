


from fastapi import status

class AppBaseException(Exception):
    
    def __init__(self, message: str, status_code: int):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)

class NotFoundError(AppBaseException):
    def __init__(self, message="Resource not found"):
        super().__init__(message, status.HTTP_404_NOT_FOUND)



class InternalServerError(AppBaseException):
    def __init__(self, message="An internal server error occurred"):
        super().__init__(message, status.HTTP_500_INTERNAL_SERVER_ERROR)

class ConflictError(AppBaseException):
    def __init__(self, message="It already exists"):
        super().__init__(message, status.HTTP_409_CONFLICT)

class InvalidCredentials(AppBaseException):
    def __init__(self, message="Invalid credentials"):
        super().__init__(message, status.HTTP_401_UNAUTHORIZED)



class InvalidFileError(AppBaseException):
    def __init__(self, message="Invalid file"):
        super().__init__(message, status.HTTP_400_BAD_REQUEST)
        
class PermissionDenied(AppBaseException):
    def __init__(self, message="Permission denied"):
        super().__init__(
            message,
            status.HTTP_403_FORBIDDEN,
        )
class ValidationError(AppBaseException):
    def __init__(self, message="Validation failed"):
        super().__init__(
            message,
            status.HTTP_422_UNPROCESSABLE_ENTITY,
        )
    
