#!/usr/bin/env python3
"""
Backend startup script with proper error handling and graceful shutdown
"""
import sys
import os
import signal
import subprocess
import time
import logging
from pathlib import Path

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Get the backend directory
BACKEND_DIR = Path(__file__).parent.absolute()
os.chdir(BACKEND_DIR)

# Add backend to path
sys.path.insert(0, str(BACKEND_DIR))

logger.info(f"Starting SIH WATER AI Backend")
logger.info(f"Backend directory: {BACKEND_DIR}")
logger.info(f"Python executable: {sys.executable}")
logger.info(f"Python version: {sys.version}")

def main():
    """Start the backend server."""
    try:
        # Import app to verify setup
        logger.info("Importing FastAPI application...")
        from app.main import app
        logger.info("✅ FastAPI app imported successfully")
        
        # Import model manager to verify models load
        logger.info("Initializing model manager...")
        from app.ml.model_manager import get_model_manager
        model_manager = get_model_manager()
        logger.info(f"✅ Model manager initialized with {len(model_manager.models)} models")
        if model_manager.models:
            logger.info(f"   Available models: {list(model_manager.models.keys())}")
        
        # Start uvicorn
        logger.info("Starting Uvicorn server...")
        import uvicorn
        
        config = uvicorn.Config(
            app=app,
            host="127.0.0.1",
            port=8000,
            log_level="info",
            access_log=True,
            use_colors=True
        )
        
        server = uvicorn.Server(config)
        logger.info("✅ Server configured")
        logger.info("🚀 Starting server on http://127.0.0.1:8000")
        logger.info("📚 API docs available at http://127.0.0.1:8000/docs")
        
        # Run the server
        asyncio_runner = server.run()
        
    except KeyboardInterrupt:
        logger.info("Received shutdown signal")
        sys.exit(0)
    except Exception as e:
        logger.error(f"❌ Error starting backend: {e}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
