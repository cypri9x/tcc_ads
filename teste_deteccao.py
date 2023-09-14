import cv2
import time
import RPi.GPIO as GPIO

width = 320
height = 240
move_x = 0.0

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
    step_size = (end - start) / float(steps)
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
    global move_x
    if 0.45 <= angle <= 0.55:
        return
    angle = (2 * angle) - 1
    angle = angle * 2.0
    angle += move_x
    if angle > 100.0:
        angle = 100.0
    elif angle < 0.0:
        angle = 0.0
    p.ChangeDutyCycle(int(angle))
    time.sleep(0.1)
    move_x = angle    

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
