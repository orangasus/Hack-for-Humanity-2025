GET_SESSION_ERROR_RESPONSE = lambda error_message: {
    "status": "error",
    "message": str(error_message),
    "code": "SESSION_DATA_RETRIEVAL_FAILED"
}
