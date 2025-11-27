"""
Supabase Service - Handles database operations
"""
import logging
from typing import Dict, Any, Optional, List
from datetime import datetime
from supabase import create_client, Client
from ..config import settings

logger = logging.getLogger(__name__)


class SupabaseService:
    """Service for Supabase database operations."""
    
    def __init__(self):
        """Initialize Supabase client."""
        if not settings.SUPABASE_URL or not settings.SUPABASE_KEY:
            logger.warning("Supabase credentials not configured")
            self.client: Optional[Client] = None
        else:
            try:
                self.client = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)
                logger.info("Supabase client initialized")
            except Exception as e:
                logger.error(f"Error initializing Supabase client: {str(e)}")
                logger.warning("Continuing without Supabase client")
                self.client = None
    
    def insert_sensor_data(self, sensor_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Insert sensor reading into database."""
        if not self.client:
            logger.warning("Supabase client not available")
            return None
        
        try:
            result = self.client.table('sensors').insert(sensor_data).execute()
            return result.data[0] if result.data else None
        except Exception as e:
            logger.error(f"Error inserting sensor data: {str(e)}")
            return None
    
    def insert_prediction(self, prediction_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Insert prediction result into database."""
        if not self.client:
            logger.warning("Supabase client not available")
            return None
        
        try:
            result = self.client.table('predictions').insert(prediction_data).execute()
            return result.data[0] if result.data else None
        except Exception as e:
            logger.error(f"Error inserting prediction: {str(e)}")
            return None
    
    def insert_model_metadata(self, model_metadata: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Insert model metadata into database."""
        if not self.client:
            logger.warning("Supabase client not available")
            return None
        
        try:
            result = self.client.table('models').insert(model_metadata).execute()
            return result.data[0] if result.data else None
        except Exception as e:
            logger.error(f"Error inserting model metadata: {str(e)}")
            return None
    
    def insert_report_metadata(self, report_metadata: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Insert report metadata into database."""
        if not self.client:
            logger.warning("Supabase client not available")
            return None
        
        try:
            result = self.client.table('reports').insert(report_metadata).execute()
            return result.data[0] if result.data else None
        except Exception as e:
            logger.error(f"Error inserting report metadata: {str(e)}")
            return None
    
    def get_recent_sensors(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Get recent sensor readings."""
        if not self.client:
            return []
        
        try:
            result = self.client.table('sensors')\
                .select('*')\
                .order('timestamp', desc=True)\
                .limit(limit)\
                .execute()
            return result.data or []
        except Exception as e:
            logger.error(f"Error fetching sensors: {str(e)}")
            return []
    
    def get_recent_predictions(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Get recent predictions."""
        if not self.client:
            return []
        
        try:
            result = self.client.table('predictions')\
                .select('*')\
                .order('timestamp', desc=True)\
                .limit(limit)\
                .execute()
            return result.data or []
        except Exception as e:
            logger.error(f"Error fetching predictions: {str(e)}")
            return []
    
    def get_active_models(self) -> List[Dict[str, Any]]:
        """Get all active models."""
        if not self.client:
            return []
        
        try:
            result = self.client.table('models')\
                .select('*')\
                .eq('is_active', True)\
                .order('training_date', desc=True)\
                .execute()
            return result.data or []
        except Exception as e:
            logger.error(f"Error fetching models: {str(e)}")
            return []
    
    def upload_file_to_storage(self, bucket: str, file_path: str, file_content: bytes) -> Optional[str]:
        """Upload file to Supabase Storage."""
        if not self.client:
            logger.warning("Supabase client not available")
            return None
        
        try:
            # Use service role client for storage operations
            from supabase import create_client as create_supabase_client
            service_client = create_supabase_client(
                settings.SUPABASE_URL,
                settings.SUPABASE_SERVICE_ROLE_KEY or settings.SUPABASE_KEY
            )
            
            # Upload the file
            try:
                service_client.storage.from_(bucket).upload(file_path, file_content, {
                    "content-type": "application/pdf"
                })
                logger.info(f"File uploaded to {bucket}/{file_path}")
            except Exception as upload_error:
                if "already exists" in str(upload_error).lower():
                    logger.warning(f"File already exists: {file_path}, will update")
                    service_client.storage.from_(bucket).update(file_path, file_content, {
                        "content-type": "application/pdf"
                    })
                else:
                    raise upload_error
            
            # Get public URL
            try:
                public_url_response = service_client.storage.from_(bucket).get_public_url(file_path)
                
                # Handle different response formats
                if isinstance(public_url_response, dict):
                    public_url = public_url_response.get('publicUrl') or public_url_response.get('url')
                else:
                    public_url = str(public_url_response)
                
                logger.info(f"Public URL: {public_url}")
                return public_url
            except Exception as url_error:
                logger.error(f"Error getting public URL: {str(url_error)}")
                # Fallback: construct URL manually
                return f"{settings.SUPABASE_URL}/storage/v1/object/public/{bucket}/{file_path}"
            
        except Exception as e:
            logger.error(f"Error uploading file to storage: {str(e)}", exc_info=True)
            return None

