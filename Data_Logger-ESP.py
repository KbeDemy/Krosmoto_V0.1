import serial
import sqlite3
from datetime import datetime

ser = serial.Serial('/dev/ttyUSB0', 9600)

conn = sqlite3.connect('sensor_data.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS sensor_data (
    timestamp TEXT,
    value INTEGER
)
''')

print("Logging gestart...")

while True:
    line = ser.readline().decode().strip()
    if line.isdigit():
        value = int(line)
        timestamp = datetime.now().isoformat()
        cursor.execute("INSERT INTO sensor_data (timestamp, value) VALUES (?, ?)", (timestamp, value))
        conn.commit()
        print(f"{timestamp} - {value}")
