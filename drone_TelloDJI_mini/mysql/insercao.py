# https://www.geeksforgeeks.org/retrieve-image-and-file-stored-as-a-blob-from-mysql-table-using-python/
# https://www.codegrepper.com/code-examples/sql/how+to+connect+python+with+mysql
# https://pynative.com/python-mysql-blob-insert-retrieve-file-image-as-a-blob-in-mysql/
# https://www.geeksforgeeks.org/how-to-read-image-from-sql-using-python/
# insert - https://pynative.com/python-mysql-blob-insert-retrieve-file-image-as-a-blob-in-mysql/
# 
'''
CREATE TABLE imagem (id INT NOT NULL PRIMARY Key , nome TEXT NOT NULL , imagem BLOB NOT NULL , biodata BLOB NOT NULL)
'''
import mysql.connector

def convertToBinaryData(filename):
    # Convert digital data to binary format
    with open(filename, 'rb') as file:
        binaryData = file.read()
    return binaryData


def insertBLOB(name, photo):
    print("Inserting BLOB into python_employee table")
    try:
        connection = mysql.connector.connect(host='localhost',database='test',user='root', )

        cursor = connection.cursor()
        sql_insert_blob_query = """ INSERT INTO imagem (nome, imagem) VALUES (%s,%s)"""

        empPicture = convertToBinaryData(photo)

        # Convert data into tuple format
        insert_blob_tuple = (name, empPicture)
        result = cursor.execute(sql_insert_blob_query, insert_blob_tuple)
        connection.commit()
        print("Image and file inserted successfully as a BLOB into python_employee table", result)

    except mysql.connector.Error as error:
        print("Failed inserting BLOB data into MySQL table {}".format(error))

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")
            
            
insertBLOB("Capoeira", "berimbau.png")           