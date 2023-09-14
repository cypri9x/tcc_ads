import cv2
from gpiozero import AngularServo
import time

# Conecte o servo angular à porta GPIO 17 (ou outra porta de sua escolha)
servo = AngularServo(18, min_angle=0, max_angle=180, initial_angle=0, min_pulse_width=0.5/1000.0, max_pulse_width=2.5/1000.0)

# Ajuste para um movimento mais rápido e suave
step = 5
delay = 0.01

width = 640
height = 480
move_x = 90
move_y = 90

video = cv2.VideoCapture(0, cv2.CAP_V4L)
video.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
video.set(cv2.CAP_PROP_FRAME_WIDTH, width)
classificador = cv2.CascadeClassifier('./classificadores/haarcascade_frontalface_default.xml')


def set_angle_x(angle):
    global move_x
    if 0.4 <= angle <= 0.6:
        return
    angle = (2 * angle) - 1
    angle = angle * 10
    
    move_x += int(angle)
    if move_x >= 180 or move_x <= 0:
        move_x = 180
        return
    elif move_x <= 0:
        move_x = 0  
        return

    servo.angle = move_x
    time.sleep(0.01)

def set_angle_y(angle):
    global move_y
    if 0.4 <= angle <= 0.6:
        return
    angle = (2 * angle) - 1
    angle = angle * 1
    
    move_y += int(angle)
    if move_y >= 180 or move_y <= 0:
        move_y = 180
        return
    elif move_y <= 0:
        move_y = 0  
        return

    servo.angle = move_y
    time.sleep(0.01)

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
        lado_movimento_y = centro_y - height // 2
        lado_movimento_y = float(lado_movimento_y) / float(height)
        set_angle_y(lado_movimento_y)

        print(lado_movimento_x)
        cv2.rectangle(imagem, (x, y), (x + l, y + a), (0, 255, 255), 2)

    cv2.imshow("Faces encontradas", imagem)

    if cv2.waitKey(1) == ord('q'):
        break

video.release()
cv2.destroyAllWindows()

servo.close()
