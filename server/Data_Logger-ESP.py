import serial
import sqlite3
import json
from datetime import datetime
import os

DB_PATH = os.path.abspath('sensor_data.db')
print(f"Logger gebruikt database: {DB_PATH}")

ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)

conn = sqlite3.connect(DB_PATH, check_same_thread=False)
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS sensor_data (
    timestamp TEXT,
    value TEXT
)
''')
conn.commit()

print("Logging gestart...")

while True:
    line = ser.readline().decode(errors='ignore').strip()
    if not line:
        continue
    print(f"Received line: {line}")
    try:
        data = json.loads(line)
        speed = data.get('speed')
        rpm = data.get('rpm')
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        if speed is not None and rpm is not None:
            value = f"speed:{speed},rpm:{rpm}"
            print("Trying to insert data into DB...")
            cursor.execute('INSERT INTO sensor_data (timestamp, value) VALUES (?, ?)', (timestamp, value))
            conn.commit()
            print(f"Data logged: {timestamp} - Speed: {speed}, RPM: {rpm}")

    except json.JSONDecodeError:
        print(f"Fout bij het decoderen van JSON: {line}")
    except Exception as e:
        print(f"Fout bij het verwerken van data: {e}")
