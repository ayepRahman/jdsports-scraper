
import pymongo
import os
import json

data_name = ['nike', 'puma', 'adidas,adidas-originals']
db_name = 'sneakus'

user = os.environ.get('mongo_user')
password = os.environ.get('mongo_password')
url = f'mongodb://127.0.0.1:27017/{db_name}'
client = pymongo.MongoClient(url)
db = client[db_name]
products = db.products
print(client.list_database_names())  # output: ['admin', 'local']
print(db.list_collection_names())  # output: []

with open(f'src/data/{data_name[2]}_data.json') as json_file:
    products_json = json.load(json_file)
    print('products_json >>>', products_json)
    products.insert_many(products_json)
