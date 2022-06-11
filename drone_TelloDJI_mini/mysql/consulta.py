# Import the required modules
import mysql.connector
import base64
from PIL import Image
import io 
import cv2

def write_file(data, filename):
    with open(filename, 'wb') as f:
        f.write(data)

def read_file(filename):
    with open(filename, 'rb') as f:
        photo = f.read()
    return photo
    
# Create a connection
mydb = mysql.connector.connect(host='localhost',database='test',user='root', )

# Create a cursor object
cursor = mydb.cursor()
  
# Prepare the query
query = 'SELECT imagem FROM imagem WHERE ID=1'
  
# Execute the query to get the file
cursor.execute(query)
  
data = cursor.fetchall()
  
# The returned data will be a list of list
image = data[0][0]
  
# Decode the string
binary_data = base64.b64decode(image)
# Convert the bytes into a PIL image
##image = Image.open(io.BytesIO(binary_data))
  
#write_file(binary_data, "foto.png")  

cv2.imshow('image', img)


