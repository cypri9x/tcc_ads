import cv2
import time
import RPi.GPIO as GPIO
import threading


width = 640
height = 480
angle_x = 0
angle_y = 0

video = cv2.VideoCapture(0, cv2.CAP_V4L)
video.set(cv2.CAP_PROP_FRAME_HEIGHT,height)
video.set(cv2.CAP_PROP_FRAME_WIDTH,width)
classificador = cv2.CascadeClassifier('./classificadores/haarcascade_frontalface_default.xml')
#classificadorOlhos = cv2.CascadeClassifier('./classificadores/haarcascade_eye.xml')

GPIO.setmode(GPIO.BOARD)
GPIO.setup(11,GPIO.OUT)
pwm_x = GPIO.PWM(11,50)
GPIO.setup(12,GPIO.OUT)
pwm_y = GPIO.PWM(12,50)

pwm_x.start(0)
pwm_y.start(0)

def set_angle_x(angle):
    global angle_x
    angle = angle % 100.0

    if angle_x != angle:
        pwm_x.ChangeDutyCycle(angle)
        time.sleep(0.5)
        pwm_x.ChangeDutyCycle(0)
        angle_x = angle
        time.sleep(1)   



while True:
    conectado, imagem = video.read()
    imagemCinza = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)
    
    facesDetectadas = classificador.detectMultiScale(imagemCinza)
    if len(facesDetectadas) > 0:
        x,y,l,a = facesDetectadas[0]
        centro_x = x + l // 2
        centro_y = y + a // 2
        lado_movimento_x = centro_x - width // 2
        lado_movimento_y = centro_y - height // 2
        set_angle_x(lado_movimento_x)
        #set_angle_y(lado_movimento_y)
        print(lado_movimento_x,",",lado_movimento_y)
        cv2.rectangle(imagem, (x, y), (x + l, y + a), (0, 255, 255), 2)
    
    #for (x, y, l, a) in facesDetectadas:
        #regiao = imagem[y:y + a, x:x + l]
        #regiaoCinzaOlho = cv2.cvtColor(regiao, cv2.COLOR_BGR2GRAY)
        #olhosDetectados = classificadorOlhos.detectMultiScale(regiaoCinzaOlho)
        
        #for (ox, oy, o1, oa) in olhosDetectados:
            #cv2.rectangle(regiao, (ox, oy), (ox + o1, oy + oa), (0, 0, 255), 2)
        
        #cv2.rectangle(imagem, (x, y), (x + l, y + a), (0, 255, 255), 2)
        
    cv2.imshow("Faces encontradas", imagem)
    
    if cv2.waitKey(1) == ord('q'):
        break

video.release()
cv2.destroyAllWindows()
