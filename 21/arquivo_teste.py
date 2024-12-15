import cv2
import numpy as np
# Informações gerais
# - A tecla para fechar foi trocada para o espaço
# - Foi testados com outras cores 

cap = cv2.VideoCapture(0) # Carregamento da camera
while True: # Carregamento dos frames
    _, frame = cap.read() # Leitura do frame
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) # Conversão do formato padrão de cor

    # Amarelo
    low_yellow = np.array([25, 70, 45])  # Configurações para o amarelo
    high_yellow = np.array([35, 255, 255])  # Configurações para o amarelo
    yellow_mask = cv2.inRange(hsv_frame, low_yellow, high_yellow) # filtro que só mostra branco onde há amarelo e o resto fica preto
    yellow = cv2.bitwise_and(frame, frame, mask=yellow_mask) # filtro que só mostra a cor amarelo e o resto fica preto

    # Roxo
    low_purple = np.array([100, 100, 100])  # Configurações para o roxo
    high_purple = np.array([160, 255, 255])  # Configurações para o roxo
    purple_mask = cv2.inRange(hsv_frame, low_purple, high_purple) # filtro que só mostra branco onde há roxo e o resto fica preto
    purple = cv2.bitwise_and(frame, frame, mask=purple_mask) # filtro que só mostra a cor roxo e o resto fica preto

    # Rosa
    low_pink = np.array([130, 100, 100]) # Configurações para o rosa
    high_pink = np.array([179, 255, 255]) # Configurações para o rosa
    pink_mask = cv2.inRange(hsv_frame, low_pink, high_pink) # filtro que só mostra branco onde há rosa e o resto fica preto
    pink = cv2.bitwise_and(frame, frame, mask=pink_mask) # filtro que só mostra a cor rosa e o resto fica preto

    # Preto e branco
    low_black = np.array([0, 0, 0])  # Configurações para o preto e branco
    high_black = np.array([150, 200, 120])  # Configurações para o preto e branco
    bl = cv2.inRange(hsv_frame, low_black, high_black) # filtro que deixa em preto e branco

    cv2.imshow("Frame", frame) # Mostra o frame
    cv2.imshow("Black and white", bl) # Mostra o frame
    #cv2.imshow("Yellow mask", yellow_mask) # Mostra o frame com filtro que mostra o branco no lugar do amarelo e o resto preto
    #cv2.imshow("Yellow", yellow) # Mostra o frame com filtro que só mostra o amarelo e o resto preto
    #cv2.imshow("Purple mask", purple_mask) # Mostra o frame com filtro que mostra o branco no lugar do roxo e o resto preto
    #cv2.imshow("Purple", purple) # Mostra o frame com filtro que só mostra o roxo e o resto preto
    #cv2.imshow("Pink mask", pink_mask) # Mostra o frame com filtro que mostra o branco no lugar do rosa e o resto preto
    #cv2.imshow("Pink", pink) # Mostra o frame com filtro que só mostra o rosa e o resto preto
    
    key = cv2.waitKey(1) # Chave para parar a camera
    if key == 32: # Valor ascii para o space
        break # Quando o space é clicado a camera fecha