import RPi.GPIO as GPIO
import time
import mysql.connector

# GPIO 핀 설정
PIR_PIN = 18  # PIR 센서에 연결된 GPIO 핀 번호
GPIO.setmode(GPIO.BCM)
GPIO.setup(PIR_PIN, GPIO.IN)

# 사람 수 초기화
person_count = 0

# MySQL 데이터베이스 연결 설정
db = mysql.connector.connect(
    host="localhost",
    user="giuje",  # MariaDB 사용자 이름
    password="rldnwp123",  # MariaDB 비밀번호
    database="mydb1"  # 사용할 데이터베이스 이름
)

cursor = db.cursor()

# 데이터베이스에 데이터 삽입 함수
def insert_person_count(person_count):
    sql = "INSERT INTO tablePIR (person_count) VALUES (%s)"   #테이블 이름 tablePIR 임
    val = (person_count,)
    cursor.execute(sql, val)
    db.commit()
    print(cursor.rowcount, "record inserted.")

try:
    print("PIR 센서 동작 시작")
    while True:
        if GPIO.input(PIR_PIN):  # PIR 센서로부터 입력을 읽어옴
            nowtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            print("현재시간 : {}".format(nowtime))
            # 사람이 감지될 때
            print("사람이 감지되었습니다.")
            person_count += 1  # 사람 수 증가
            print("현재 감지한 사람 수:", person_count)

            # 데이터베이스에 사람 수 삽입
            insert_person_count(person_count)

            time.sleep(3)  # 3초간 대기하여 반복적인 감지 방지
        else:
            # 감지되지 않을 때
            print("감지되지 않음")
            time.sleep(1)

except KeyboardInterrupt:
    print("키보드 인터럽트가 감지되었습니다. 정리 중...")
finally:
    cursor.close()
    db.close()
    GPIO.cleanup()
