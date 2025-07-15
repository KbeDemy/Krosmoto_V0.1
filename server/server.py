from flask import Flask, render_template, jsonify, request
import sqlite3

app = Flask(__name__)

def get_data():
    conn = sqlite3.connect('sensor_data.db')  # make database connection
    cursor = conn.cursor()
    cursor.execute("SELECT rowid, value, timestamp FROM sensor_data ORDER BY timestamp DESC LIMIT 20")
    data = cursor.fetchall()
    conn.close()
    return data

def insert_data(speed, rpm):
    conn = sqlite3.connect('sensor_data.db') 
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO sensor_data (value, timestamp) VALUES (?, datetime('now'))",
        (f"speed:{speed},rpm:{rpm}",)
    )
    conn.commit()
    conn.close()

    # Opgelet: je mag hier **geen jsonify() returnen** als dit buiten een route gebeurt!
    # Dat doe je in de route-functie zelf.
    return

@app.route('/')
def index():
    data = get_data()
    return render_template('index.html', data=data)

@app.route('/log', methods=['POST'])
def log_data():
    data = request.get_json()  # JSON uitlezen van ESP32
    speed = data['speed']
    rpm = data['rpm']
    insert_data(speed, rpm)
    return jsonify({'status': 'ok'})  #  response naar ESP32

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
