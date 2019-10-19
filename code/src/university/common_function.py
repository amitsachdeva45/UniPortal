import pymongo
from django.conf import settings

def get_id(collection):
    myclient = pymongo.MongoClient(settings.CLIENT)
    mydb = myclient[settings.DATABASE]
    mycol = mydb[collection]
    id = mycol.find_and_modify(query= { '_id': "id"},update= { '$inc': {'seq': 1}}, new=True ).get('seq')
    return int(id)

def insert_one(collection, data):
    myclient = pymongo.MongoClient(settings.CLIENT)
    mydb = myclient[settings.DATABASE]
    mycol = mydb[collection]
    mycol.insert_one(data)

def get_all(collection, data):
    myclient = pymongo.MongoClient(settings.CLIENT)
    mydb = myclient[settings.DATABASE]
    mycol = mydb[collection]
    return mycol.find(data)


def get_find_one(collection, data):
    myclient = pymongo.MongoClient(settings.CLIENT)
    mydb = myclient[settings.DATABASE]
    mycol = mydb[collection]
    return mycol.find_one(data)

def update_one(collection, whereCond, updateCond):
    myclient = pymongo.MongoClient(settings.CLIENT)
    mydb = myclient[settings.DATABASE]
    mycol = mydb[collection]
    return mycol.update_one(whereCond, updateCond, upsert=False)

def delete_one(collection, data):
    myclient = pymongo.MongoClient(settings.CLIENT)
    mydb = myclient[settings.DATABASE]
    mycol = mydb[collection]
    return mycol.delete_one(data)