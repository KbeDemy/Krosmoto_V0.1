from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

def get_data():
    conn = sqlite3.connect('sensor_data.db')  # Zelfde als logger!
    cursor = conn.cursor()
    cursor.execute("SELECT rowid, value, timestamp FROM sensor_data ORDER BY timestamp DESC LIMIT 20")
    data = cursor.fetchall()
    conn.close()
    return data

@app.route('/')
def index():
    data = get_data()
    return render_template('index.html', data=data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)



