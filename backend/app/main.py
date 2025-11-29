"""
Main FastAPI Application for SIH WATER AI
"""
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging
import time
import signal
import sys
import platform

from .config import settings
from .api.routes import router
from .utils.responses import error_response, success_response
from .utils.rate_limiter import allow_request, get_window_usage

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configure resource limits for stability (Unix/Linux only)
if platform.system() != "Windows":
    try:
        import resource
        # Increase file descriptor limit to prevent exhaustion
        soft, hard = resource.getrlimit(resource.RLIMIT_NOFILE)
        resource.setrlimit(resource.RLIMIT_NOFILE, (4096, hard))
        logger.info(f"Set file descriptor limit: {soft} -> 4096")
    except Exception as e:
        logger.warning(f"Could not set resource limits: {str(e)}")
else:
    logger.info("Running on Windows - skipping resource limit configuration")

# Signal handlers for graceful shutdown
def handle_shutdown(signum, frame):
    logger.info(f"Received shutdown signal {signum} - allowing graceful shutdown")
    # Don't immediately exit - let asyncio handle it
    pass

# Only register signal handlers on non-Windows systems
if platform.system() != "Windows":
    signal.signal(signal.SIGTERM, handle_shutdown)
    signal.signal(signal.SIGINT, handle_shutdown)

# Create FastAPI app
app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Industrial Wastewater Treatment Optimization System with AI",
    version="1.0.0"
)

# CORS middleware
allowed_origins = [
    "http://localhost:3000",
    "http://localhost:8000",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:8000",
]

# Add production URLs if provided
import os
if os.getenv("FRONTEND_URL"):
    allowed_origins.append(os.getenv("FRONTEND_URL"))

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins if os.getenv("ENV") == "production" else ["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)


# Request logging middleware for performance monitoring
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all HTTP requests with timing information."""
    start_time = time.time()
    try:
        # Rate limiting: per-client IP
        client_ip = request.client.host if request.client else 'unknown'
        allowed, retry_after = allow_request(client_ip)
        if not allowed:
            # Return 429 Too Many Requests
            content = error_response(
                message=f"Rate limit exceeded. Try again in {retry_after} seconds",
                status_code=429,
                details={"retry_after": retry_after}
            )
            return JSONResponse(status_code=429, content=content)
        response = await call_next(request)
        process_time = time.time() - start_time
        logger.info(
            f"{request.method} {request.url.path} - "
            f"Status: {response.status_code} - "
            f"Duration: {process_time:.3f}s"
        )
        response.headers["X-Process-Time"] = str(process_time)
        return response
    except Exception as e:
        process_time = time.time() - start_time
        logger.error(
            f"{request.method} {request.url.path} - "
            f"Error: {str(e)} - Duration: {process_time:.3f}s",
            exc_info=True
        )
        raise

# Include routers
app.include_router(router, prefix=settings.API_V1_STR, tags=["api"])


@app.on_event("startup")
async def startup_event():
    """Initialize services on startup."""
    try:
        # Initialize model manager first (required for API)
        from .ml.model_manager import get_model_manager
        model_manager = get_model_manager()
        logger.info(f"Model manager initialized with {len(model_manager.models)} models")
        
        # Initialize MQTT service (optional)
        try:
            from .services.mqtt_service import get_mqtt_service
            mqtt_service = get_mqtt_service()
            logger.info("MQTT service initialized")
        except Exception as mqtt_error:
            logger.warning(f"MQTT service not available: {str(mqtt_error)}")
        
    except Exception as e:
        logger.warning(f"Error during startup: {str(e)}")


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown."""
    try:
        from .services.mqtt_service import _mqtt_service
        if _mqtt_service:
            _mqtt_service.disconnect()
            logger.info("MQTT service disconnected")
    except Exception as e:
        logger.warning(f"Error during shutdown: {str(e)}")


@app.get("/")
async def root():
    """Root endpoint with system information."""
    return success_response(
        {
            "service": "SIH WATER AI",
            "version": "1.0.0",
            "description": "Industrial Wastewater Treatment Optimization System",
            "docs": "/docs",
            "health_check": "/health"
        },
        "SIH WATER AI Service"
    )


@app.get("/health")
async def health_check():
    """
    Comprehensive health check endpoint.
    Returns system status, model availability, and dependencies.
    """
    try:
        # Check model manager
        from .ml.model_manager import get_model_manager
        model_manager = get_model_manager()
        available_models = list(model_manager.models.keys())
        models_status = "healthy" if available_models else "warning"
        
        # Check Supabase
        from .services.supabase_service import SupabaseService
        supabase_service = SupabaseService()
        supabase_status = "healthy" if supabase_service.client else "unavailable"
        
        # Check MQTT (optional)
        try:
            from .services.mqtt_service import get_mqtt_service
            mqtt_service = get_mqtt_service()
            mqtt_status = "connected" if mqtt_service and mqtt_service.client else "disconnected"
        except:
            mqtt_status = "unavailable"
        
        health_data = {
            "service": "SIH WATER AI",
            "status": "healthy",
            "timestamp": time.time(),
            "version": "1.0.0",
            "dependencies": {
                "models": {
                    "status": models_status,
                    "available": len(available_models),
                    "models": available_models
                },
                "database": {
                    "status": supabase_status,
                    "type": "Supabase PostgreSQL"
                },
                "mqtt": {
                    "status": mqtt_status,
                    "type": "Mosquitto (optional)"
                }
            }
        }
        
        return success_response(health_data, "System healthy")
        
    except Exception as e:
        logger.error(f"Health check error: {str(e)}", exc_info=True)
        return error_response(f"Health check failed: {str(e)}", 503)


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler with standardized error response."""
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content=error_response(
            "Internal server error",
            status_code=500,
            details={"exception": str(exc)[:100]}  # Limit detail length
        )
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )

