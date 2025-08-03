import sqlite3
import sys
from config import DB_PATH


# DB 및 테이블 생성
def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sensor_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            temperature REAL,
            humidity REAL,
            light REAL
        )
    ''')
    conn.commit()
    conn.close()
    print("✅ DB 및 테이블이 초기화되었습니다.")

# 더미 데이터 삽입
def insert_dummy_data():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    dummy_values = [
        ('2025-08-01 12:00:00', 25.3, 60.5, 300.0),
        ('2025-08-01 13:00:00', 26.1, 58.2, 280.0),
        ('2025-08-01 14:00:00', 27.0, 55.0, 320.0),
    ]

    cursor.executemany('''
        INSERT INTO sensor_data (timestamp, temperature, humidity, light)
        VALUES (?, ?, ?, ?)
    ''', dummy_values)

    conn.commit()
    conn.close()
    print("✅ 더미 데이터가 삽입되었습니다.")

# 모든 센서 데이터 삭제
def delete_all_sensor_data():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    # 테이블 데이터 삭제
    cursor.execute('DELETE FROM sensor_data')
    # AUTOINCREMENT 초기화 (id를 1부터 다시 시작하게 함)
    cursor.execute('DELETE FROM sqlite_sequence WHERE name="sensor_data"')
    conn.commit()
    conn.close()
    print("🗑️ 모든 센서 데이터가 삭제되었고, ID 시퀀스가 초기화되었습니다.")

# 메인 조건 분기
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("❗ 사용법: python model_sensor.py [init|insert|delete]")
        sys.exit(1)

    command = sys.argv[1].lower()

    if command == 'init':
        init_db()
    elif command == 'insert':
        insert_dummy_data()
    elif command == 'delete':
        delete_all_sensor_data()
    else:
        print(f"❗ 알 수 없는 명령어: {command}")
        print("사용 가능한 명령어: init | insert | delete")