import RPi.GPIO as GPIO
import time
import Adafruit_DHT as dht
import mysql.connector

# DHT22 센서를 GPIO 핀 4에 연결합니다.
DHT_PIN = 4
LED_PIN = 24

# MySQL 데이터베이스 연결 설정
db = mysql.connector.connect(
    host="localhost",
    user="giuje",  # MariaDB 사용자 이름
    password="rldnwp123",  # MariaDB 비밀번호
    database="mydb1"  # 사용할 데이터베이스 이름
)

cursor = db.cursor()

# 데이터베이스에 데이터 삽입 함수
def insert_sensor_value(sensor_id, temperature, humidity):
    sql = "INSERT INTO tableDHT22 (sensor_id, temperature, humidity) VALUES (%s, %s, %s)"
    val = (sensor_id, temperature, humidity)
    cursor.execute(sql, val)
    db.commit()
    print(cursor.rowcount, "record inserted.")

GPIO.setmode(GPIO.BCM)
GPIO.setup(DHT_PIN, GPIO.IN)
GPIO.setup(LED_PIN, GPIO.OUT)

sensor_id = "DHT22_1"  # 센서 ID

try:
    while True:
        try:
            nowtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            humidity, temperature_c = dht.read_retry(dht.DHT22, DHT_PIN)
            if temperature_c is not None:
                temperature_f = temperature_c * (9 / 5) + 32  # 화씨온도 f = 섭씨온도 c + 32
                print("현재시간 : {}".format(nowtime))
                print(
                    "온도: {:.1f} F / {:.1f} C  습도: {:.1f}% ".format(temperature_f, temperature_c, humidity)
                )

                # 데이터베이스에 값 삽입
                insert_sensor_value(sensor_id, temperature_c, humidity)

                if temperature_c >= 25:
                    print("<<<에어컨 작동 요망>>>")
                    GPIO.output(LED_PIN, GPIO.HIGH)
                elif temperature_c <= 17:
                    print("<<<난방기 작동 요망>>>")
                    GPIO.output(LED_PIN, GPIO.HIGH)
                else:
                    GPIO.output(LED_PIN, GPIO.LOW)
            else:
                print("온도 데이터 실패")

        except RuntimeError as error:
            print(error.args[0])
            time.sleep(2.0)
            continue
        except Exception as error:
            raise error

        time.sleep(2.0)

except KeyboardInterrupt:
    print("Script stopped by user")

finally:
    cursor.close()
    db.close()
    GPIO.cleanup()
