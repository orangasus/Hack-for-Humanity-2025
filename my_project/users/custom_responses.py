USERNAME_TAKEN_RESPONSE = {
    "status": "error",
    "message": "Username already taken",
    "code": "USERNAME_TAKEN"
}

EMAIL_TAKEN_RESPONSE = {
    "status": "error",
    "message": "Email already taken",
    "code": "EMAIL_TAKEN"
}

USER_SIGNUP_RESPONSE = {
    "status": "success",
    "message": "User signed up successfully",
    "code": "USER_SIGNED_UP"
}

USER_SIGNUP_ERROR = lambda error_message: {
    "status": "error",
    "message": str(error_message),
    "code": "USER_SIGNUP_ERROR"
}

INTEGRITY_ERROR_RESPONSE = {
    "status": "error",
    "message": "Database integrity error",
    "code": "DATABASE_INTEGRITY_ERROR"
}

RESET_PASSWORD_REQUEST_RESPONSE = {
    "status": "success",
    "message": "Password reset request successful",
    "code": "PASSWORD_RESET_REQUEST_SUCCESS"
}

RESET_PASSWORD_REQUEST_ERROR = lambda error_message: {
    "status": "error",
    "message": str(error_message),
    "code": "PASSWORD_RESET_REQUEST_FAILED"
}

RESET_PASSWORD_CHECK_TOKEN_RESPONSE = lambda can_reset: {
    "status": "success",
    "message": "Password reset token verified",
    "code": "PASSWORD_RESET_TOKEN_VERIFIED",
    "can_reset_password": can_reset
}

RESET_PASSWORD_CHECK_TOKEN_ERROR = lambda error_message: {
    "status": "error",
    "message": str(error_message),
    "code": "PASSWORD_RESET_TOKEN_VERIFICATION_FAILED",
    "can_reset_password": False
}

PASSWORD_CHANGED = {
    "status": "success",
    "message": "Password changed successfully",
    "code": "PASSWORD_CHANGED"
}

PASSWORD_CHANGED_ERROR = lambda error_message: {
    "status": "error",
    "message": str(error_message),
    "code": "PASSWORD_CHANGE_FAILED"
}

SERVER_ERROR_RESPONSE = lambda error_message: {
    "status": "error",
    "message": str(error_message),
    "code": "SERVER_ERROR"
}

USER_CREATED_RESPONSE = {
    "status": "success",
    "message": "User created successfully",
    "code": "USER_CREATED"
}

USER_DELETED_RESPONSE = {
    "status": "success",
    "message": "User deleted successfully",
    "code": "USER_DELETED"
}

USER_DELETED_ERROR = lambda error_message: {
    "status": "error",
    "message": str(error_message),
    "code": "USER_DELETE_FAILED"
}

USER_FOUND_RESPONSE = lambda user_data: {
    "status": "success",
    "message": "User found successfully",
    "code": "USER_FOUND",
    "data": user_data
}

USER_NOT_FOUND_RESPONSE = {
    "status": "error",
    "message": "User not found",
    "code": "USER_NOT_FOUND"
}

USER_UPDATED_RESPONSE = {
    "status": "success",
    "message": "User updated successfully",
    "code": "USER_UPDATED"
}

USER_UPDATE_ERROR = lambda error_message: {
    "status": "error",
    "message": str(error_message),
    "code": "USER_UPDATE_FAILED"
}

INVALID_CREDENTIALS_RESPONSE = {
    "status": "error",
    "message": "Invalid credentials",
    "code": "INVALID_CREDENTIALS"
}

USER_LOGGED_IN_RESPONSE = {
    "status": "success",
    "message": "User logged in successfully",
    "code": "USER_LOGGED_IN",
}

AUTH_ERROR = lambda error_message: {
    "status": "error",
    "message": str(error_message),
    "code": "USER_LOGIN_FAILED"
}

LOGOUT_SUCCESS_RESPONSE = {
    "status": "success",
    "message": "User logged out successfully",
    "code": "USER_LOGGED_OUT"
}

LOGOUT_ERROR_RESPONSE = lambda error_message: {
    "status": "error",
    "message": str(error_message),
    "code": "USER_LOGOUT_FAILED"
}

SET_SESSION_SUCCESS_RESPONSE = {
    "status": "success",
    "message": "Session data set successfully",
    "code": "SESSION_DATA_SET"
}

SET_SESSION_ERROR_RESPONSE = lambda error_message: {
    "status": "error",
    "message": str(error_message),
    "code": "SESSION_DATA_SET_FAILED"
}

GET_SESSION_SUCCESS_RESPONSE = lambda value: {
    "status": "success",
    "message": f"Session data retrieved: {value}",
    "code": "SESSION_DATA_RETRIEVED",
    "data": value
}

GET_SESSION_ERROR_RESPONSE = lambda error_message: {
    "status": "error",
    "message": str(error_message),
    "code": "SESSION_DATA_RETRIEVAL_FAILED"
}

DELETE_SESSION_SUCCESS_RESPONSE = {
    "status": "success",
    "message": "Session data cleared successfully",
    "code": "SESSION_DATA_CLEARED"
}

DELETE_SESSION_ERROR_RESPONSE = lambda error_message: {
    "status": "error",
    "message": str(error_message),
    "code": "SESSION_DATA_CLEAR_FAILED"
}