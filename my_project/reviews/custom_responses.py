# reviews/custom_responses.py

LATEST_REVIEWS_RESPONSE = lambda data: {
    "status": "success",
    "message": "Latest reviews retrieved successfully",
    "code": "LATEST_REVIEWS",
    "data": data
}

REVIEW_CREATED_RESPONSE = lambda data: {
    "status": "success",
    "message": "Review created successfully",
    "code": "REVIEW_CREATED",
    "data": data
}

REVIEW_CREATION_ERROR = lambda errors: {
    "status": "error",
    "message": str(errors),
    "code": "REVIEW_CREATION_FAILED"
}

REVIEW_RETRIEVED_RESPONSE = lambda data: {
    "status": "success",
    "message": "Review retrieved successfully",
    "code": "REVIEW_RETRIEVED",
    "data": data
}

REVIEW_UPDATED_RESPONSE = lambda data: {
    "status": "success",
    "message": "Review updated successfully",
    "code": "REVIEW_UPDATED",
    "data": data
}

REVIEW_UPDATE_ERROR = lambda errors: {
    "status": "error",
    "message": str(errors),
    "code": "REVIEW_UPDATE_FAILED"
}

REVIEW_DELETED_RESPONSE = {
    "status": "success",
    "message": "Review deleted successfully",
    "code": "REVIEW_DELETED"
}

REVIEW_DELETION_ERROR = lambda errors: {
    "status": "error",
    "message": str(errors),
    "code": "REVIEW_DELETION_FAILED"
}

REVIEW_NOT_FOUND_RESPONSE = {
    "status": "error",
    "message": "Review not found",
    "code": "REVIEW_NOT_FOUND"
}
