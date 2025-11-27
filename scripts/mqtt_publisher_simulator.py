"""
MQTT Publisher Simulator
Simulates realistic sensor data for testing
"""
import json
import time
import random
import paho.mqtt.client as mqtt
import sys
from datetime import datetime

# Configuration
BROKER_URL = "localhost"
BROKER_PORT = 1883
PUBLISH_INTERVAL = 5  # seconds

# Sensor types and their realistic value ranges
SENSORS = {
    "temperature": {
        "min": 15.0,
        "max": 35.0,
        "unit": "°C",
        "variation": 0.5
    },
    "ph": {
        "min": 6.5,
        "max": 8.5,
        "unit": "pH",
        "variation": 0.1
    },
    "bod": {
        "min": 50.0,
        "max": 500.0,
        "unit": "mg/L",
        "variation": 10.0
    },
    "cod": {
        "min": 100.0,
        "max": 1000.0,
        "unit": "mg/L",
        "variation": 20.0
    },
    "dissolved_oxygen": {
        "min": 2.0,
        "max": 8.0,
        "unit": "mg/L",
        "variation": 0.2
    },
    "ammonia": {
        "min": 0.5,
        "max": 50.0,
        "unit": "mg/L",
        "variation": 1.0
    },
    "nitrate": {
        "min": 0.1,
        "max": 30.0,
        "unit": "mg/L",
        "variation": 0.5
    },
    "turbidity": {
        "min": 1.0,
        "max": 100.0,
        "unit": "NTU",
        "variation": 2.0
    },
    "tss": {
        "min": 10.0,
        "max": 500.0,
        "unit": "mg/L",
        "variation": 5.0
    },
    "flow_rate": {
        "min": 500.0,
        "max": 2000.0,
        "unit": "LPM",
        "variation": 50.0
    }
}


class SensorSimulator:
    """Simulates sensor readings with realistic patterns."""
    
    def __init__(self):
        """Initialize simulator with base values."""
        self.base_values = {}
        for sensor_type, config in SENSORS.items():
            self.base_values[sensor_type] = random.uniform(
                config["min"],
                config["max"]
            )
    
    def generate_reading(self, sensor_type: str) -> dict:
        """Generate a realistic sensor reading."""
        if sensor_type not in SENSORS:
            return None
        
        config = SENSORS[sensor_type]
        base_value = self.base_values[sensor_type]
        
        # Add realistic variation
        variation = random.uniform(-config["variation"], config["variation"])
        value = base_value + variation
        
        # Clamp to valid range
        value = max(config["min"], min(config["max"], value))
        
        # Update base value (drift slowly)
        self.base_values[sensor_type] += random.uniform(-0.1, 0.1) * config["variation"]
        self.base_values[sensor_type] = max(
            config["min"],
            min(config["max"], self.base_values[sensor_type])
        )
        
        return {
            "parameter": sensor_type,
            "value": round(value, 2),
            "unit": config["unit"],
            "timestamp": datetime.now().isoformat(),
            "location": "treatment_plant_1"
        }


def publish_sensor_data(client: mqtt.Client, sensor_type: str, sensor_id: str, data: dict):
    """Publish sensor data to MQTT topic."""
    topic = f"plant/sensors/{sensor_type}/{sensor_id}"
    message = json.dumps(data)
    
    result = client.publish(topic, message)
    
    if result.rc == mqtt.MQTT_ERR_SUCCESS:
        print(f"✓ Published {sensor_type} ({sensor_id}): {data['value']} {data['unit']}")
    else:
        print(f"✗ Failed to publish {sensor_type}")


def main():
    """Main simulation loop."""
    print("=" * 60)
    print("MQTT Sensor Data Simulator")
    print("=" * 60)
    print(f"Broker: {BROKER_URL}:{BROKER_PORT}")
    print(f"Publish interval: {PUBLISH_INTERVAL} seconds")
    print("=" * 60)
    print("\nPress Ctrl+C to stop\n")
    
    # Create MQTT client
    client = mqtt.Client(client_id="sensor_simulator")
    
    try:
        # Connect to broker
        print(f"Connecting to MQTT broker...")
        client.connect(BROKER_URL, BROKER_PORT, 60)
        client.loop_start()
        
        time.sleep(1)  # Wait for connection
        
        # Initialize simulator
        simulator = SensorSimulator()
        
        # Sensor IDs for each type
        sensor_ids = {
            "temperature": "temp_001",
            "ph": "ph_001",
            "bod": "bod_001",
            "cod": "cod_001",
            "dissolved_oxygen": "do_001",
            "ammonia": "nh3_001",
            "nitrate": "no3_001",
            "turbidity": "turb_001",
            "tss": "tss_001",
            "flow_rate": "flow_001"
        }
        
        # Main loop
        iteration = 0
        while True:
            iteration += 1
            print(f"\n--- Iteration {iteration} ---")
            
            # Generate and publish readings for each sensor
            for sensor_type, sensor_id in sensor_ids.items():
                reading = simulator.generate_reading(sensor_type)
                if reading:
                    publish_sensor_data(client, sensor_type, sensor_id, reading)
                    time.sleep(0.1)  # Small delay between publishes
            
            # Wait before next iteration
            time.sleep(PUBLISH_INTERVAL)
            
    except KeyboardInterrupt:
        print("\n\nStopping simulator...")
    except Exception as e:
        print(f"\nError: {str(e)}")
    finally:
        client.loop_stop()
        client.disconnect()
        print("Disconnected from MQTT broker")


if __name__ == "__main__":
    # Allow override of broker URL from command line
    if len(sys.argv) > 1:
        BROKER_URL = sys.argv[1]
    if len(sys.argv) > 2:
        BROKER_PORT = int(sys.argv[2])
    
    main()

