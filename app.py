import sqlite3
import json
from flask import Flask, Response, jsonify, send_from_directory, render_template
from config import DB_PATH

app = Flask(__name__)


# 1. 루트 페이지 (테스트용 홈)
@app.route('/')
def index():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM sensor_data ORDER BY id DESC')
    rows = cursor.fetchall()
    latest = rows[0] if rows else None
    conn.close()

    return render_template('index.html', rows=rows, latest=latest)


# 2. 센서 데이터 수신 (아두이노 → 서버)
@app.route('/sensor', methods=['GET'])
def get_sensor_data():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM sensor_data ORDER BY id DESC')
    rows = cursor.fetchall()
    conn.close()

    result = [
        {
            "id": row[0],
            "timestamp": row[1],
            "temperature": row[2],
            "humidity": row[3],
            "light": row[4]
        }
        for row in rows
    ]

    json_data = json.dumps(result, ensure_ascii=False, indent=4)
    return Response(json_data, mimetype='application/json')


# 3. 이미지 업로드 (ESP32-CAM → 서버)
@app.route('/upload-image', methods=['POST'])
def upload_image():
    # 이미지 저장 처리
    return jsonify({'status': 'image uploaded'})


# 4. 제어 명령 요청 (앱 → 서버)
@app.route('/control', methods=['POST'])
def control_device():
    # 팬, 펌프, LED 등 제어 명령 처리
    return jsonify({'status': 'control command received'})


# 5. 이미지 파일 조회 (웹에서 보기 용도)
@app.route('/image/<filename>')
def get_image(filename):
    # 저장된 이미지 파일 반환
    return send_from_directory('images', filename)


if __name__ == '__main__':
    app.run(debug=True)