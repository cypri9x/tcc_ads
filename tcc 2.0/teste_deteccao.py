import cv2

classificador = cv2.CascadeClassifier('classificadores\haarcascade_frontalface_default.xml')

imagem = cv2.imread('./imagens/pessoas2.jpg') 
imagemCinza = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)


cv2.waitKey()


facesDetectadas = classificador.detectMultiScale(imagemCinza)


print(len(facesDetectadas))

print(facesDetectadas)

for (x,y,l,a) in facesDetectadas:
    cv2.rectangle(imagem, (x,y), (x+l, y + a), (0,255,255),2)

cv2.imshow("Faces Encontradas", imagem)
cv2.waitKey()