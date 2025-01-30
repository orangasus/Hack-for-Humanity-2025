UNIVERSITY_CREATED_RESPONSE = lambda data: {
    "status": "success",
    "message": "University created successfully",
    "data": data,
    "code": "UNIVERSITY_CREATED"
}

UNIVERSITY_CREATION_ERROR = lambda errors: {
    "status": "error",
    "message": "Error creating university",
    "errors": errors,
    "code": "UNIVERSITY_CREATION_ERROR"
}

PROFESSOR_CREATED_RESPONSE = lambda data: {
    "status": "success",
    "message": "Professor created successfully",
    "data": data,
    "code": "PROFESSOR_CREATED"
}

PROFESSOR_CREATION_ERROR = lambda errors: {
    "status": "error",
    "message": "Error creating professor",
    "errors": errors,
    "code": "PROFESSOR_CREATION_ERROR"
}

PROFESSOR_RATING_UPDATED_RESPONSE = {
    "status": "success",
    "message": "Professor rating updated successfully",
    "code": "PROFESSOR_RATING_UPDATED"
}

PROFESSOR_RATING_UPDATE_ERROR = lambda errors: {
    "status": "error",
    "message": "Error updating professor rating",
    "errors": errors,
    "code": "PROFESSOR_RATING_UPDATE_ERROR"
}

UNI_INFO_BY_ID_RESPONSE = lambda uni, profs, courses: {
    "status": "success",
    "message": "We rly need pages",
    "code": "UNI_INFO_BY_ID_SUCCESS",
    "university": uni,
    "professors": profs,
    "courses": courses
}