import serial
import sqlite3
import json
from datetime import datetime

ser = serial.Serial('/dev/ttyUSB0', 9600)

conn = sqlite3.connect('sensor_data.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS sensor_data (
    timestamp TEXT,
    value TEXT
)
''')

print("Logging gestart...")

while True:
    line = ser.readline().decode().strip()
    try:
        data = json.loads(line)
        speed = data.get('speed')
        rpm = data.get('rpm')
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        if speed is not None and rpm is not None:
            value = f"speed:{speed},rpm:{rpm}"
            cursor.execute('INSERT INTO sensor_data (timestamp, value) VALUES (?, ?)', (timestamp, value))
            conn.commit()
        print(f"Data logged: {timestamp} - Speed: {speed}, RPM: {rpm}")

    except json.JSONDecodeError:
        print(f"Fout bij het decoderen van JSON: {line}")
    except Exception as e:
        print(f"Fout bij het verwerken van data: {e}")
