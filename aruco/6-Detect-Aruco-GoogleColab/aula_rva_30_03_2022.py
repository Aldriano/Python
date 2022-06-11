# -*- coding: utf-8 -*-
"""Aula_RVA_30_03_2022.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1dv8-0cNI2M2BOxh6G3irOZ2CdqQlzHZg
"""

!python --version

import cv2
from cv2 import aruco
import numpy as np
from google.colab.patches import cv2_imshow
from IPython.display import display, Javascript
from google.colab.output import eval_js
from base64 import b64decode
from IPython.display import clear_output 

# get current DateTime
from datetime import datetime

def take_photo(filename='photo.jpg', quality=0.8):
  js = Javascript('''
    async function takePhoto(quality) {
      const div = document.createElement('div');

      const video = document.createElement('video');
      video.style.display = 'hidden';
      const stream = await navigator.mediaDevices.getUserMedia({video: true});

      document.body.appendChild(div);
      div.appendChild(video);
      video.srcObject = stream;
      await video.play();

      const canvas = document.createElement('canvas');
      canvas.width = video.videoWidth;
      canvas.height = video.videoHeight;
      canvas.getContext('2d').drawImage(video, 0, 0);
      stream.getVideoTracks()[0].stop();
      div.remove();
      return canvas.toDataURL('image/jpeg', quality);
    }
    ''')
  display(js)
  data = eval_js('takePhoto({})'.format(quality))
  binary = b64decode(data.split(',')[1])
  with open(filename, 'wb') as f:
    f.write(binary)
  return filename

# download imagem
!wget https://aldriano.com.br/imagens/debian-logo.png

imgAug = cv2.imread("debian-logo.png")

# observar o dicionário do aruco - 6x6_250
def findArucoMarkers(img, markerSize = 6, totalMarkers=250, draw=True):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    key = getattr(aruco, f'DICT_{markerSize}X{markerSize}_{totalMarkers}') #dicionario 6x6
    arucoDict = aruco.Dictionary_get(key)
    arucoParam = aruco.DetectorParameters_create()
    bboxs, ids, rejected = aruco.detectMarkers(gray, arucoDict, parameters = arucoParam)
    # print(ids)
    if draw:
        aruco.drawDetectedMarkers(img, bboxs)
    return [bboxs, ids]

def arucoAug(bbox, id, img, imgAug, drawnId=True): 
    tl = bbox[0][0][0], bbox[0][0][1]
    tr = bbox[0][1][0], bbox[0][1][1]
    br = bbox[0][2][0], bbox[0][2][1]
    bl = bbox[0][3][0], bbox[0][3][1]

    h, w, c = imgAug.shape

    pts1 = np.array([tl, tr, br, bl])
    pts2 = np.float32([[0,0], [w,0], [w,h], [0, h]])

    matrix, _ = cv2.findHomography(pts2, pts1)

    imgout = cv2.warpPerspective(imgAug, matrix, (img.shape[1],img.shape[0]))

    cv2.fillConvexPoly(img, pts1.astype(int), (0,0,0))

    imgout = img + imgout
    
    return imgout

while True:
    dt = str(datetime.now())
    nomeImagem = dt.replace(":","-")

    take_photo()

    imgCapturada = cv2.imread('photo.jpg')
    #img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    arucofound = findArucoMarkers(imgCapturada)

    # loop through all the markers and augment each one
    if  len(arucofound[0])!=0:
        #for bbox, id in zip(arucofound[0], arucofound[1]):
        #    imgCapturada = arucoAug(bbox, id, imgCapturada, imgAug)
            
        for bbox, id in zip(arucofound[0], arucofound[1]):
          imgCapturada = arucoAug(bbox, id, imgCapturada, imgAug)
          if imgCapturada is None:
              imgCapturada = imgCapturada
          else:
              imgCapturada += imgCapturada
    
    clear_output()

    print('ids=', arucofound[1])
    cv2_imshow(imgCapturada)
    if arucofound[1] is not None:
       imgSalva = "img-"+nomeImagem+".jpg"
       cv2.imwrite(imgSalva,imgCapturada)