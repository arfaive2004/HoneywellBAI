from energyplus.sensor_manager import SensorManager

sensor = SensorManager(".")

state = sensor.get_latest_state()

for k, v in state.items():
    print(f"{k}: {v}")