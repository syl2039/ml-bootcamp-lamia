import cv2
import numpy as np

cap = cv2.VideoCapture(0) # Carregamento da camera
while True: # Carregamento dos frames
    _, frame = cap.read() # Leitura do frame
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) # Conversão do formato padrão de cor

    # Vermelho
    low_red = np.array([100, 100, 60]) # Configurações para o vermelho1
    high_red = np.array([179, 255, 255]) # Configurações para o vermelho
    red_mask = cv2.inRange(hsv_frame, low_red, high_red) # filtro que só mostra branco onde há vermelho e o resto fica preto
    red = cv2.bitwise_and(frame, frame, mask=red_mask) # filtro que só mostra a cor vermelha e o resto fica preto

    # Azul
    low_blue = np.array([94, 80, 2]) # Configurações para o azul
    high_blue = np.array([126, 255, 255]) # Configurações para o azul
    blue_mask = cv2.inRange(hsv_frame, low_blue, high_blue) # filtro que só mostra branco onde há azul e o resto fica preto
    blue = cv2.bitwise_and(frame, frame, mask=blue_mask) # filtro que só mostra a cor azul e o resto fica preto

    # Verde
    low_green = np.array([25, 25, 72]) # Configurações para o green
    high_green = np.array([102, 255, 255]) # Configurações para o green
    green_mask = cv2.inRange(hsv_frame, low_green, high_green) # filtro que só mostra branco onde há green e o resto fica preto
    green = cv2.bitwise_and(frame, frame, mask=green_mask) # filtro que só mostra a cor green e o resto fica preto

    # Sem branco
    low = np.array([0, 42, 0]) # Configurações para tirar o branco
    high = np.array([179, 255, 255]) # Configurações para tirar o branco
    mask = cv2.inRange(hsv_frame, low, high) # filtro que tira o branco
    result = cv2.bitwise_and(frame, frame, mask=mask) # filtro que tira o branco

    cv2.imshow("Frame", frame) # Mostra o frame
    cv2.imshow("No white", result) # Mostra o frame
    #cv2.imshow("Red mask", red_mask) # Mostra o frame com filtro que mostra o branco no lugar do vermelho e o resto preto
    #cv2.imshow("Red ", red) # Mostra o frame com filtro que mostra apenas vermelho e o resto preto
    #cv2.imshow("Blue mask", blue_mask) # Mostra o frame com filtro que mostra o branco no lugar do azul e o resto preto
    #cv2.imshow("Blue ", blue) # Mostra o frame com filtro que mostra apenas o azul e o resto preto
    #cv2.imshow("Green mask", green_mask) # Mostra o frame com filtro que mostra o branco no lugar do verde e o resto preto
    #cv2.imshow("Green ", green) # Mostra o frame com filtro que mostra apenas o verde e o resto preto
    

    key = cv2.waitKey(1) # Chave para parar a camera
    if key == 27: # Valor ascii para o esc
        break # Quando o esc é clicado a camera fecha