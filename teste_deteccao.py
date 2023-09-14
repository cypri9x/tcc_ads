import cv2
import time
import RPi.GPIO as GPIO

width = 320
height = 240

video = cv2.VideoCapture(0, cv2.CAP_V4L)
video.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
video.set(cv2.CAP_PROP_FRAME_WIDTH, width)
classificador = cv2.CascadeClassifier('./classificadores/haarcascade_frontalface_default.xml')

GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.OUT)
p = GPIO.PWM(11, 50)
p.start(0)

def move_motor_smoothly(start, end, duration):
    steps = 100
    step_size = (end - start) / steps
    delay = duration / steps
    for _ in range(steps):
        start += step_size
        p.ChangeDutyCycle(start)
        time.sleep(delay)

def set_angle_x_bkp(angle):
    if 0.45 <= angle <= 0.55:
        return
    angle = max(0.0, min(1.0, angle))
    angle = 2.0 + angle * 10.0
    move_motor_smoothly(angle, angle * 10.0, 1.0)

def set_angle_x(angle):
    if 0.45 <= angle <= 0.55:
        return
    angle = max(0.0, min(1.0, angle))
    angle = 2.0 + angle * 10.0
    move_motor_smoothly(0, angle * 10.0, 1.0)    

while True:
    conectado, imagem = video.read()
    imagemCinza = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)

    facesDetectadas = classificador.detectMultiScale(imagemCinza)
    if len(facesDetectadas) > 0:
        x, y, l, a = facesDetectadas[0]
        centro_x = x + l // 2
        centro_y = y + a // 2
        lado_movimento_x = centro_x - width // 2
        lado_movimento_x = float(lado_movimento_x) / float(width)
        set_angle_x(lado_movimento_x)

        print(lado_movimento_x)
        cv2.rectangle(imagem, (x, y), (x + l, y + a), (0, 255, 255), 2)

    cv2.imshow("Faces encontradas", imagem)

    if cv2.waitKey(1) == ord('q'):
        break

video.release()
cv2.destroyAllWindows()

p.stop()
GPIO.cleanup()
