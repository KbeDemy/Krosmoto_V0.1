from flask import Flask, render_template, jsonify
import sqlite3
import os

app = Flask(__name__)

DB_PATH = os.path.abspath('sensor_data.db')
print(f"Server gebruikt database: {DB_PATH}")

def get_data():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT rowid, value, timestamp FROM sensor_data ORDER BY timestamp DESC LIMIT 20")
    data = cursor.fetchall()
    conn.close()
    return data

@app.route('/')
def index():
    data = get_data()
    return render_template('index.html', data=data)

@app.route('/api/latest')
def api_latest():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT value, timestamp FROM sensor_data ORDER BY timestamp DESC LIMIT 1")
    row = cursor.fetchone()
    conn.close()

    if row:
        try:
            value_str, timestamp = row
            parts = dict(item.split(":") for item in value_str.split(","))
            speed = int(parts.get("speed", 0))
            rpm = int(parts.get("rpm", 0))
            return jsonify({"speed": speed, "rpm": rpm, "timestamp": timestamp})
        except Exception as e:
            return jsonify({"error": "Parse error", "details": str(e)}), 500
    else:
        return jsonify({"error": "No data found"}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
