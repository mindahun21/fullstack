from rest_framework.views import exception_handler
from rest_framework import status

def custom_exception_handler(exc, context):
    """
    Returns a consistent JSON error body format:
    {
        "status": <http_status_code>,
        "message": "<human_readable_message>",
        "errors": <optional_field_errors>
    }
    """
    response = exception_handler(exc, context)

    if response is not None:
        status_code = response.status_code
        error_data = response.data

        if status_code == status.HTTP_404_NOT_FOUND:
            message = "Resource not found."
        elif status_code == status.HTTP_400_BAD_REQUEST:
            message = "Validation error: invalid request payload."
        elif status_code == status.HTTP_405_METHOD_NOT_ALLOWED:
            message = "Method not allowed on this endpoint."
        else:
            message = getattr(exc, 'detail', 'An error occurred processing your request.')
            if isinstance(message, list) or isinstance(message, dict):
                message = "An error occurred."

        formatted_response = {
            "status": status_code,
            "message": str(message),
            "errors": error_data if isinstance(error_data, dict) else {"detail": error_data}
        }
        response.data = formatted_response

    return response
