
from pymongo import MongoClient
from google.colab.patches import cv2_imshow
import cv2
import base64
import numpy

client = MongoClient('mongodb+srv://alunos:senha@cluster0.wwa6n.mongodb.net')

result = client.RVA.imagens.find_one({'id_img': 1})
img = base64.b64decode(result['img'])
file_bytes = numpy.asarray(bytearray(img), dtype=numpy.uint8)
img = cv2.imdecode(file_bytes, 1)
cv2_imshow(img)