"""
MQTT Service - Handles MQTT message subscription and publishing
"""
import json
import logging
from typing import Dict, Any, Optional, Callable
import paho.mqtt.client as mqtt
from ..config import settings
from ..services.supabase_service import SupabaseService

logger = logging.getLogger(__name__)


class MQTTService:
    """Service for MQTT communication."""
    
    def __init__(self):
        """Initialize MQTT client."""
        self.client: Optional[mqtt.Client] = None
        self.supabase_service = SupabaseService()
        self.is_connected = False
        self.message_callback: Optional[Callable] = None
        self._reconnect_attempts = 0
        self._max_reconnect_attempts = 5
        
    def connect(self):
        """Connect to MQTT broker."""
        try:
            self.client = mqtt.Client(client_id="sih_water_ai_backend", protocol=mqtt.MQTTv311)
            
            # Set callbacks
            self.client.on_connect = self._on_connect
            self.client.on_message = self._on_message
            self.client.on_disconnect = self._on_disconnect
            
            # Set credentials if provided
            if settings.MQTT_USERNAME and settings.MQTT_PASSWORD:
                self.client.username_pw_set(settings.MQTT_USERNAME, settings.MQTT_PASSWORD)
            
            # Connect with timeout
            logger.info(f"Connecting to MQTT broker: {settings.MQTT_BROKER_URL}:{settings.MQTT_BROKER_PORT}")
            self.client.connect(settings.MQTT_BROKER_URL, settings.MQTT_BROKER_PORT, 60)
            
            # Start loop
            self.client.loop_start()
            
        except ConnectionRefusedError:
            logger.warning(f"MQTT broker not available at {settings.MQTT_BROKER_URL}:{settings.MQTT_BROKER_PORT}. MQTT features disabled.")
            self.is_connected = False
            self.client = None
        except Exception as e:
            logger.warning(f"MQTT connection error: {str(e)}. Continuing without MQTT support.", exc_info=False)
            self.is_connected = False
            self.client = None
    
    def _on_connect(self, client, userdata, flags, rc):
        """Callback when connected to broker."""
        if rc == 0:
            self.is_connected = True
            logger.info("Connected to MQTT broker")
            
            # Subscribe to sensor topics
            topic = "plant/sensors/#"
            client.subscribe(topic)
            logger.info(f"Subscribed to topic: {topic}")
        else:
            logger.error(f"Failed to connect to MQTT broker. Return code: {rc}")
            self.is_connected = False
    
    def _on_message(self, client, userdata, msg):
        """Callback when message is received."""
        try:
            topic = msg.topic
            payload = msg.payload.decode('utf-8')
            
            logger.info(f"Received message on topic: {topic}")
            
            # Parse JSON payload
            try:
                data = json.loads(payload)
            except json.JSONDecodeError:
                logger.warning(f"Invalid JSON payload: {payload}")
                return
            
            # Extract sensor information from topic
            # Topic format: plant/sensors/{sensor_type}/{sensor_id}
            topic_parts = topic.split('/')
            sensor_type = topic_parts[2] if len(topic_parts) > 2 else 'unknown'
            sensor_id = topic_parts[3] if len(topic_parts) > 3 else 'unknown'
            
            # Prepare sensor record
            sensor_record = {
                'sensor_id': sensor_id,
                'sensor_type': sensor_type,
                'parameter_name': data.get('parameter', sensor_type),
                'value': data.get('value', 0.0),
                'unit': data.get('unit'),
                'location': data.get('location'),
                'metadata': {
                    'topic': topic,
                    'raw_data': data
                }
            }
            
            # Store in database
            self.supabase_service.insert_sensor_data(sensor_record)
            
            # Call custom callback if set
            if self.message_callback:
                self.message_callback(sensor_record)
                
        except Exception as e:
            logger.error(f"Error processing MQTT message: {str(e)}")
    
    def _on_disconnect(self, client, userdata, rc):
        """Callback when disconnected."""
        self.is_connected = False
        logger.warning(f"Disconnected from MQTT broker. Return code: {rc}")
    
    def subscribe(self, topic: str, callback: Optional[Callable] = None):
        """Subscribe to a topic."""
        if not self.client or not self.is_connected:
            logger.warning("MQTT client not connected")
            return
        
        self.client.subscribe(topic)
        logger.info(f"Subscribed to topic: {topic}")
        
        if callback:
            self.message_callback = callback
    
    def publish(self, topic: str, payload: Dict[str, Any]):
        """Publish message to a topic."""
        if not self.client or not self.is_connected:
            logger.warning("MQTT client not connected")
            return False
        
        try:
            message = json.dumps(payload)
            result = self.client.publish(topic, message)
            
            if result.rc == mqtt.MQTT_ERR_SUCCESS:
                logger.info(f"Published message to topic: {topic}")
                return True
            else:
                logger.error(f"Failed to publish message. Return code: {result.rc}")
                return False
                
        except Exception as e:
            logger.error(f"Error publishing message: {str(e)}")
            return False
    
    def disconnect(self):
        """Disconnect from MQTT broker."""
        try:
            if self.client:
                self.client.loop_stop()
                self.client.disconnect()
                self.is_connected = False
                logger.info("Disconnected from MQTT broker")
        except Exception as e:
            logger.error(f"Error during disconnect: {str(e)}", exc_info=True)
            self.is_connected = False


# Global MQTT service instance
_mqtt_service: Optional[MQTTService] = None


def get_mqtt_service() -> MQTTService:
    """Get or create global MQTT service instance."""
    global _mqtt_service
    if _mqtt_service is None:
        _mqtt_service = MQTTService()
        _mqtt_service.connect()
    return _mqtt_service

