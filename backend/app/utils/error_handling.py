"""
Standardized Error Handling and Response Formatting
"""
from typing import Optional, Dict, Any
from datetime import datetime
from enum import Enum


class ErrorCode(str, Enum):
    """Standard error codes for the API."""
    VALIDATION_ERROR = "VALIDATION_ERROR"
    NOT_FOUND = "NOT_FOUND"
    UNAUTHORIZED = "UNAUTHORIZED"
    FORBIDDEN = "FORBIDDEN"
    CONFLICT = "CONFLICT"
    INTERNAL_ERROR = "INTERNAL_ERROR"
    BAD_REQUEST = "BAD_REQUEST"
    MODEL_ERROR = "MODEL_ERROR"
    DATABASE_ERROR = "DATABASE_ERROR"
    MQTT_ERROR = "MQTT_ERROR"
    SERVICE_UNAVAILABLE = "SERVICE_UNAVAILABLE"


class StandardErrorResponse:
    """Standardized error response wrapper."""
    
    @staticmethod
    def create(
        message: str,
        error_code: ErrorCode,
        status_code: int,
        details: Optional[Dict[str, Any]] = None,
        request_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Create a standardized error response.
        
        Args:
            message: User-friendly error message
            error_code: Machine-readable error code
            status_code: HTTP status code
            details: Additional error details
            request_id: Request tracking ID
            
        Returns:
            Standardized error response dict
        """
        return {
            "success": False,
            "message": message,
            "error_code": error_code.value,
            "status_code": status_code,
            "details": details or {},
            "timestamp": datetime.utcnow().isoformat(),
            "request_id": request_id
        }
    
    @staticmethod
    def validation_error(
        message: str = "Validation failed",
        details: Optional[Dict] = None,
        request_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Create a validation error response."""
        return StandardErrorResponse.create(
            message=message,
            error_code=ErrorCode.VALIDATION_ERROR,
            status_code=422,
            details=details,
            request_id=request_id
        )
    
    @staticmethod
    def not_found(
        message: str = "Resource not found",
        resource_type: Optional[str] = None,
        request_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Create a not found error response."""
        details = {}
        if resource_type:
            details["resource_type"] = resource_type
        return StandardErrorResponse.create(
            message=message,
            error_code=ErrorCode.NOT_FOUND,
            status_code=404,
            details=details,
            request_id=request_id
        )
    
    @staticmethod
    def unauthorized(
        message: str = "Unauthorized",
        request_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Create an unauthorized error response."""
        return StandardErrorResponse.create(
            message=message,
            error_code=ErrorCode.UNAUTHORIZED,
            status_code=401,
            request_id=request_id
        )
    
    @staticmethod
    def forbidden(
        message: str = "Forbidden",
        request_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Create a forbidden error response."""
        return StandardErrorResponse.create(
            message=message,
            error_code=ErrorCode.FORBIDDEN,
            status_code=403,
            request_id=request_id
        )
    
    @staticmethod
    def internal_error(
        message: str = "Internal server error",
        exception: Optional[str] = None,
        request_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Create an internal error response."""
        details = {}
        if exception:
            details["exception"] = exception[:100]  # Limit length
        return StandardErrorResponse.create(
            message=message,
            error_code=ErrorCode.INTERNAL_ERROR,
            status_code=500,
            details=details,
            request_id=request_id
        )
    
    @staticmethod
    def model_error(
        message: str = "Model operation failed",
        available_models: Optional[list] = None,
        request_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Create a model error response."""
        details = {}
        if available_models is not None:
            details["available_models"] = available_models
        return StandardErrorResponse.create(
            message=message,
            error_code=ErrorCode.MODEL_ERROR,
            status_code=400,
            details=details,
            request_id=request_id
        )
    
    @staticmethod
    def database_error(
        message: str = "Database operation failed",
        request_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Create a database error response."""
        return StandardErrorResponse.create(
            message=message,
            error_code=ErrorCode.DATABASE_ERROR,
            status_code=500,
            request_id=request_id
        )
    
    @staticmethod
    def service_unavailable(
        message: str = "Service temporarily unavailable",
        details: Optional[Dict] = None,
        request_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Create a service unavailable response."""
        return StandardErrorResponse.create(
            message=message,
            error_code=ErrorCode.SERVICE_UNAVAILABLE,
            status_code=503,
            details=details,
            request_id=request_id
        )
