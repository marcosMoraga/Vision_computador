import cv2
import numpy as np
import time

cap = cv2.VideoCapture(0)
cap1 = cv2.VideoCapture(1)
path = './'
dif = 0
cont = 0
azulBajo = np.array([100,100,20],np.uint8)
azulAlto = np.array([125,255,255],np.uint8)

while True:
    ret, frame = cap.read()
    ret1, frame1 = cap1.read()
    #rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    #C3 = rgb[:, :, 2]
    frameHSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    frameHSV1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(frameHSV,azulBajo,azulAlto)
    mask2 = cv2.inRange(frameHSV1,azulBajo,azulAlto)

    cv2.imshow('Cam', frame)
    cv2.imshow('Cam2', frame1)
    
    cont +=1
    if(cont%2==0):
        cv2.imwrite(path + 'IMG_2.jpg', mask)
        cv2.imwrite(path + 'IMG_4.jpg', mask2)
    else:
        cv2.imwrite(path + 'IMG_1.jpg', mask)
        cv2.imwrite(path + 'IMG_3.jpg', mask2)
    if(cont>=2):
        foto1 = cv2.imread('IMG_1.jpg')
        foto2 = cv2.imread('IMG_2.jpg')
        foto3 = cv2.imread('IMG_3.jpg')
        foto4 = cv2.imread('IMG_4.jpg')
        diferencia = cv2.absdiff(foto1,foto2)
        diferencia2 = cv2.absdiff(foto3,foto4)
        rgb = cv2.cvtColor(diferencia, cv2.COLOR_BGR2RGB)
        rgb2 = cv2.cvtColor(diferencia2, cv2.COLOR_BGR2RGB)
        azul = rgb[:, :, 2]
        azul2 = rgb2[:, :, 2]
        #_,binario = cv2.threshold(azul, 255, 255, cv2.THRESH_BINARY)
        contornos,_ = cv2.findContours(azul, cv2.RETR_EXTERNAL,
                                        cv2.CHAIN_APPROX_SIMPLE)
        contornos2,_ = cv2.findContours(azul2, cv2.RETR_EXTERNAL,
                                        cv2.CHAIN_APPROX_SIMPLE)
        #diferencia = cv2.drawContours(diferencia, contornos, 0, (225,0,0), 3)
        for c in contornos:
            area = cv2.contourArea(c)
            if area > 2000:
                M = cv2.moments(c)
                if (M["m00"]==0): M["m00"]=1
                x = int(M["m10"]/M["m00"])
                y = int(M['m01']/M['m00'])
                if(y<150):
                    special = 'A'
                else:
                    special = 'B'
                cv2.circle(diferencia, (x,y), 7, (0,255,0), -1)
                font = cv2.FONT_HERSHEY_SIMPLEX
                cv2.putText(diferencia, special,(x+10,y), font, 0.75,(0,255,0),1,cv2.LINE_AA)
                nuevoContorno = cv2.convexHull(c)
                cv2.drawContours(diferencia, [nuevoContorno], 0, (255,0,0), 3)
        for c in contornos2:
            area = cv2.contourArea(c)
            if area > 2000:
                M = cv2.moments(c)
                if (M["m00"]==0): M["m00"]=1
                x = int(M["m10"]/M["m00"])
                y = int(M['m01']/M['m00'])
                special = 'C'
                cv2.circle(diferencia2, (x,y), 7, (0,255,0), -1)
                font = cv2.FONT_HERSHEY_SIMPLEX
                cv2.putText(diferencia2, special,(x+10,y), font, 0.75,(0,255,0),1,cv2.LINE_AA)
                nuevoContorno = cv2.convexHull(c)
                cv2.drawContours(diferencia2, [nuevoContorno], 0, (255,0,0), 3)
        cv2.imshow('Contornos',diferencia)
        cv2.imshow('Contornos2',diferencia2)
        time.sleep(0.1)
    if cv2.waitKey(1) & 0xFF == ord('s'):
        break
cv2.destroyAllWindows()