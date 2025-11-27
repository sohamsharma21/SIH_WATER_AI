"""
Standardized Response Formatting Functions
"""
from typing import Dict, Any, Optional, List
from datetime import datetime


def success_response(
    data: Any,
    message: str = "Success",
    status_code: int = 200
) -> Dict[str, Any]:
    """
    Create a standardized success response.
    
    Args:
        data: Response data
        message: Success message
        status_code: HTTP status code
        
    Returns:
        Formatted success response
    """
    return {
        "success": True,
        "message": message,
        "data": data,
        "status_code": status_code,
        "timestamp": datetime.utcnow().isoformat()
    }


def error_response(
    message: str,
    status_code: int = 400,
    error_code: Optional[str] = None,
    details: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Create a standardized error response.
    
    Args:
        message: Error message
        status_code: HTTP status code
        error_code: Machine-readable error code
        details: Additional error details
        
    Returns:
        Formatted error response
    """
    return {
        "success": False,
        "message": message,
        "error_code": error_code or f"ERROR_{status_code}",
        "status_code": status_code,
        "details": details or {},
        "timestamp": datetime.utcnow().isoformat()
    }


def created_response(
    data: Any,
    message: str = "Created successfully",
    status_code: int = 201
) -> Dict[str, Any]:
    """
    Create a 201 Created response.
    
    Args:
        data: Created resource data
        message: Success message
        status_code: HTTP status code (default 201)
        
    Returns:
        Formatted creation response
    """
    return success_response(data, message, status_code)


def validation_error_response(
    message: str = "Validation failed",
    details: Optional[Dict[str, Any]] = None,
    status_code: int = 422
) -> Dict[str, Any]:
    """
    Create a validation error response.
    
    Args:
        message: Error message
        details: Validation error details
        status_code: HTTP status code
        
    Returns:
        Formatted validation error response
    """
    return error_response(
        message=message,
        status_code=status_code,
        error_code="VALIDATION_ERROR",
        details=details
    )


def not_found_response(
    message: str = "Resource not found",
    resource_type: Optional[str] = None,
    status_code: int = 404
) -> Dict[str, Any]:
    """
    Create a 404 Not Found response.
    
    Args:
        message: Error message
        resource_type: Type of resource not found
        status_code: HTTP status code
        
    Returns:
        Formatted not found response
    """
    details = {}
    if resource_type:
        details["resource_type"] = resource_type
    
    return error_response(
        message=message,
        status_code=status_code,
        error_code="NOT_FOUND",
        details=details
    )


def paginated_response(
    data: List[Any],
    total: int,
    page: int = 1,
    page_size: int = 50,
    message: str = "Success"
) -> Dict[str, Any]:
    """
    Create a paginated response.
    
    Args:
        data: List of items
        total: Total number of items
        page: Current page number
        page_size: Items per page
        message: Success message
        
    Returns:
        Formatted paginated response
    """
    total_pages = (total + page_size - 1) // page_size
    
    return {
        "success": True,
        "message": message,
        "data": data,
        "pagination": {
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": total_pages
        },
        "timestamp": datetime.utcnow().isoformat()
    }


def internal_error_response(
    message: str = "Internal server error",
    exception: Optional[str] = None,
    status_code: int = 500
) -> Dict[str, Any]:
    """
    Create an internal error response.
    
    Args:
        message: Error message
        exception: Exception details (limited to 100 chars)
        status_code: HTTP status code
        
    Returns:
        Formatted error response
    """
    details = {}
    if exception:
        details["exception"] = exception[:100]
    
    return error_response(
        message=message,
        status_code=status_code,
        error_code="INTERNAL_ERROR",
        details=details
    )
