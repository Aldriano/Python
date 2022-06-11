def get_database():
    import certifi
    from pymongo import MongoClient
    import pymongo
    ca = certifi.where()

    CONNECTION_STRING = "mongodb+srv://name:xxxxxx@cluster0.i3wmm.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"

    from pymongo import MongoClient
    client = MongoClient(CONNECTION_STRING, tlsCAFile=ca)

    return client.provaAula

def getImgFromDb():    
    # pega db
    dbname = get_database()
    collection_name =  dbname["imagesAula"]
    
    img = ''
    item_details = collection_name.find()
    for item in item_details:
        img = item['img']

    return img


print(getImgFromDb())