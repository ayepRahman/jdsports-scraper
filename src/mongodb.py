
import pymongo
import os
import json


data_name = 'nike_data'
# data_name = 'adidas,adidas-originals_data'

user = os.environ.get('mongo_user')
password = os.environ.get('mongo_password')
url = 'mongodb://127.0.0.1:27017/sneakus' or f'mongodb+srv://{user}:{password}@cluster0-ysglw.mongodb.net/'
client = pymongo.MongoClient(url)
db = client.amazon_clone
products = db.products
print(client.list_database_names())  # output: ['admin', 'local']
print(db.list_collection_names())  # output: []

with open(f'src/data/{data_name}.json') as json_file:
    products_json = json.load(json_file)
    print('products_json >>>', products_json)
    products.insert_many(products_json)
