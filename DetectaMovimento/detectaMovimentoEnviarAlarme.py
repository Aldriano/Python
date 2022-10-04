# By Aldrano
# Setembro 2022
# Detector de movimento - dispara Thread com request a uma API
import cv2
import numpy as np

import requests
import threading

podeEnviarAlarme = True
    
def thread_function(nome):
    global podeEnviarAlarme

    url = "https://aldriano.com.br/.../api_add_json.php"
    try:
        response = requests.post(url, json={'nome': 'Dispositivo Corredor 72', 'mensagem': 'ALARME'})

        #print(response.ok) # True
        #print(response.status_code) #200
        
    except requests.exceptions.ConnectionError:
        print("Connection refused")
    except requests.Timeout as e:
        print("OOPS!! Timeout Error")
        print(str(e))        
    except requests.RequestException as e:
        print("OOPS!! General Error")
        print(str(e))   
    except KeyboardInterrupt:
        print("Someone closed the program")    
    finally:
        podeEnviarAlarme = True
        print(response.json())   
        
camera = cv2.VideoCapture(0)

#A dilatação expande, enquanto a erosão reduz uma imagem. – Abertura: • Suaviza o contorno da imagem
# Elemento estruturantes -  passa a forma e o tamanho do kernel, você obtém o kernel desejado
es = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9,4))
fundo = None

while (True):
    ret, frame = camera.read()
    # if frame is read correctly ret is True
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break
        
    if fundo is None:
        fundo = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) # converter em tons de cinza
        # Aplicar filtro/kernel/ gaussiano 21x21, borda = 0 - e desfocá-lo um pouco, é que, em cada
        # Captura de vídeo, há um ruído natural proveniente de vibrações naturais, mudanças na iluminação e
        # o ruído gerado pela própria câmera. Temos suavizar esse ruído para que não seja detectado como movimento
        fundo = cv2.GaussianBlur(fundo, (21, 21), 0)
        #print("fundo: ", fundo.shape)
        #cv2.imshow("fundo", fundo)
        #cv2.waitKey(0)
        continue
 
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) # Mesmo processo da imagem de fundo
    gray_frame = cv2.GaussianBlur(gray_frame, (21, 21), 0) # Mesmo processo da imagem de fundo    
    # find the absolute difference between background and current frame
    diff = cv2.absdiff(fundo, gray_frame) # obtenha um mapa de diferenças.

    #cv2.imshow("diff", diff)
    #print("diff= " ,diff)
    #cv2.waitKey(0)
    
    # Aplica um limiar, de modo a obter uma imagem em preto e branco
    # https://docs.opencv.org/4.x/d7/d1b/group__imgproc__misc.html#ggaa9e58d2860d4afa658ef70a9b1115576a147222a96556ebc1d948b372bcd7ac59
    # https://www.geeksforgeeks.org/python-thresholding-techniques-using-opencv-set-1-simple-thresholding/
    # limiar/thresh T=25 if src(x,y) < T dst(x,y) = 0 else dst(x,y) = 255
    diff = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)[1]
    # dilatar a imagem de modo que buracos e as imperfeições são normalizadas
    # https://opencv24-python-tutorials.readthedocs.io/en/latest/py_tutorials/py_imgproc/py_morphological_ops/py_morphological_ops.html
    diff = cv2.dilate(diff, es, iterations = 2)
        
    # manual findContours  - https://docs.opencv.org/4.x/d4/d73/tutorial_py_contours_begin.html
    cnts, hierarchy = cv2.findContours(diff.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) #Calcula os contornos
    
    #print("qtd cnt= ",cnts)
    
    #verifica se LIST não esta vazio
    if cnts:
        print("Detectado movimento >>>>>>>>>>>")
        if podeEnviarAlarme:
            x = threading.Thread(target=thread_function, args=(podeEnviarAlarme,))
            x.start()
            podeEnviarAlarme = False
        else:
            print("Thread ocupado...")
    else:
        print("Nada detectado...")
    
    cv2.imshow("contours", frame)
    cv2.imshow("dif", diff)
    if cv2.waitKey(1000) & 0xff == ord("q"):
        break
cv2.destroyAllWindows()
camera.release()
