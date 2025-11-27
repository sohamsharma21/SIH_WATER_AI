# MQTT Broker Setup Guide

## Option 1: Local Mosquitto Broker (Recommended for Development)

### Windows Installation

1. **Download Mosquitto**
   - Visit: https://mosquitto.org/download/
   - Download Windows installer
   - Install with default options

2. **Start Mosquitto Service**
   ```powershell
   # Start the service
   net start mosquitto
   
   # Or run manually
   mosquitto -c mosquitto.conf
   ```

3. **Default Configuration**
   - Port: 1883 (MQTT)
   - Port: 8883 (MQTT over SSL)
   - No authentication by default

4. **Test Connection**
   ```powershell
   # Subscribe (in one terminal)
   mosquitto_sub -h localhost -t "test/topic"
   
   # Publish (in another terminal)
   mosquitto_pub -h localhost -t "test/topic" -m "Hello MQTT"
   ```

### Linux/Mac Installation

```bash
# Ubuntu/Debian
sudo apt-get install mosquitto mosquitto-clients

# macOS
brew install mosquitto

# Start service
sudo systemctl start mosquitto
# or
brew services start mosquitto
```

## Option 2: Cloud MQTT Brokers (Production)

### HiveMQ Cloud (Free Tier Available)
- URL: https://www.hivemq.com/cloud/
- Create free account
- Get broker URL and credentials
- Update `.env` file with credentials

### Eclipse Mosquitto Cloud
- URL: https://mosquitto.org/
- Similar setup process

### AWS IoT Core
- More complex setup
- Good for production deployments

## Configuration for SIH WATER AI

Update your `.env` file in the backend directory:

```env
MQTT_BROKER_URL=localhost
MQTT_BROKER_PORT=1883
MQTT_USERNAME=
MQTT_PASSWORD=
```

For cloud brokers:

```env
MQTT_BROKER_URL=broker.your-provider.com
MQTT_BROKER_PORT=8883
MQTT_USERNAME=your_username
MQTT_PASSWORD=your_password
```

## MQTT Topics Used

The application uses the following topic structure:

- `plant/sensors/temperature` - Temperature readings
- `plant/sensors/ph` - pH readings
- `plant/sensors/bod` - BOD readings
- `plant/sensors/cod` - COD readings
- `plant/sensors/#` - All sensor data (wildcard subscription)

## Testing MQTT Connection

Use the provided simulator:

```bash
cd scripts
python mqtt_publisher_simulator.py
```

This will publish sample sensor data to the broker.

