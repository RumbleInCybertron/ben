import logging
from fastapi import HTTPException, status

logger = logging.getLogger("user_auth_service")

class UserAlreadyExistsException(HTTPException):
    def __init__(self):
        logger.error("Attempt to create a user with an existing username")
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already exists"
        )

class InvalidCredentialsException(HTTPException):
    def __init__(self):
        logger.warning("Invalid login attempt")
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )

class DatabaseConnectionException(HTTPException):
    def __init__(self):
        logger.critical("Database connection failed")
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Could not connect to the database"
        )
