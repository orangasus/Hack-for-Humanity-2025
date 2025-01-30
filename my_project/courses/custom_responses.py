COURSE_RETRIEVED_RESPONSE = lambda data, profs, uni: {
    "status": "success",
    "message": "Course retrieved successfully",
    "data": data,
    "professors": profs,
    "university": uni,
    "code": "COURSE_RETRIEVED"
}

COURSE_NOT_FOUND_RESPONSE = {
    "status": "error",
    "message": "Course not found",
    "code": "COURSE_NOT_FOUND"
}

COURSE_CREATED_RESPONSE = lambda data: {
    "status": "success",
    "message": "Course created successfully",
    "data": data,
    "code": "COURSE_CREATED"
}

COURSE_CREATION_ERROR = lambda errors: {
    "status": "error",
    "message": "Error creating course",
    "errors": errors,
    "code": "COURSE_CREATION_ERROR"
}

COURSE_UPDATED_RESPONSE = lambda data: {
    "status": "success",
    "message": "Course updated successfully",
    "data": data,
    "code": "COURSE_UPDATED"
}

COURSE_UPDATE_ERROR = lambda errors: {
    "status": "error",
    "message": "Error updating course",
    "errors": errors,
    "code": "COURSE_UPDATE_ERROR"
}

COURSE_DELETED_RESPONSE = {
    "status": "success",
    "message": "Course deleted successfully",
    "code": "COURSE_DELETED"
}

COURSE_DELETION_ERROR = lambda error: {
    "status": "error",
    "message": "Error deleting course",
    "error": error,
    "code": "COURSE_DELETION_ERROR"
}

COURSE_LIST_RESPONSE = lambda data: {
    "status": "success",
    "message": "Courses retrieved successfully",
    "data": data,
    "code": "COURSE_LIST"
}

COURSE_SEARCH_RESPONSE = lambda data: {
    "status": "success",
    "message": "Course search results",
    "data": data,
    "code": "COURSE_SEARCH"
}

COURSE_RATING_UPDATED_RESPONSE = {
    "status": "success",
    "message": "Course rating updated successfully",
    "code": "COURSE_RATING_UPDATED"
}

COURSE_RATING_UPDATE_ERROR = lambda errors: {
    "status": "error",
    "message": "Error updating course rating",
    "errors": errors,
    "code": "COURSE_RATING_UPDATE_ERROR"
}
