import cv2

width = 640
height = 480
video = cv2.VideoCapture(0, cv2.CAP_V4L)
video.set(cv2.CAP_PROP_FRAME_HEIGHT,height)
video.set(cv2.CAP_PROP_FRAME_WIDTH,width)
classificador = cv2.CascadeClassifier('./classificadores/haarcascade_frontalface_default.xml')
#classificadorOlhos = cv2.CascadeClassifier('./classificadores/haarcascade_eye.xml')


while True:
    conectado, imagem = video.read()
    imagemCinza = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)
    
    facesDetectadas = classificador.detectMultiScale(imagemCinza)
    if len(facesDetectadas) > 0:
        x,y,l,a = facesDetectadas[0]
        centro_x = x + l // 2
        lado_movimento = centro_x - width // 2
        print(lado_movimento)
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
