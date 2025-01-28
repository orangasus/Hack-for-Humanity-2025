# emails/custom_responses.py

CONFIRMATION_EMAIL_SENT_RESPONSE = {
    "status": "success",
    "message": "Confirmation email sent successfully",
    "code": "CONFIRMATION_EMAIL_SENT"
}

CONFIRMATION_EMAIL_ERROR = lambda error_message: {
    "status": "error",
    "message": str(error_message),
    "code": "CONFIRMATION_EMAIL_FAILED"
}

ACCOUNT_ACTIVATED_RESPONSE = {
    "status": "success",
    "message": "Account activated successfully",
    "code": "ACCOUNT_ACTIVATED"
}

ACTIVATION_FAILED_RESPONSE = {
    "status": "error",
    "message": "Account activation failed",
    "code": "ACTIVATION_FAILED"
}

PASSWORD_RESET_EMAIL_SENT_RESPONSE = {
    "status": "success",
    "message": "Password reset email sent successfully",
    "code": "PASSWORD_RESET_EMAIL_SENT"
}

PASSWORD_RESET_EMAIL_ERROR = lambda error_message: {
    "status": "error",
    "message": str(error_message),
    "code": "PASSWORD_RESET_EMAIL_FAILED"
}