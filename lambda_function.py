import json
import os
from pymongo import MongoClient
from bson.json_util import dumps
from bson.objectid import ObjectId


# connect MongoDB
MONGO_URI = os.environ.get("MONGO_URI")

# initialize the mongo Client
client =MongoClient(host = MONGO_URI)

# select Database
db = client.get_database("crud")

# select Collection
collection = db.get_collection("data")


def lambda_handler(event, context):
    print('Request event: ', event)
    response = None
   
    try:
        http_method = event.get('httpMethod')
        # path = event.get('path')
        
        if http_method == 'GET' :
            documents = list(collection.find())
            response = build_response(200, documents)
        
        # Other Methods
        elif http_method == 'POST' :
            # response = build_response(201,loads(event['body']))
            output = create(json.loads(event['body']))
            response = build_response(201, output)
            
        elif http_method == 'PATCH' :
            item_id = event['pathParameters']['id']
            item_data = json.loads(event['body'])
            result = collection.update_one({"_id": ObjectId(item_id)}, {"$set": item_data})
            response = build_response(200, 'updated successfully')
            
        elif http_method == 'DELETE':
            item_id = event['pathParameters']['id']
            # body = json.loads(event['body']
            result = collection.delete_one({"_id": ObjectId(item_id)})
            response = build_response(201,'item deleted successfully with id '+ item_id)
            
            
        
            
        else:
            response = build_response(404, '404 Not Found')
            
            

    except Exception as e:
        print('Error:', e)
        response = build_response(400, 'Error processing request')
        
    return response 
   

# Create user
def create(data):
    if data:
        # insert documents into collection
        if isinstance(data, list) and len(data)>1:
            # return('more than 1 data')
            result = collection.insert_many(data)
        else :
            # return('data')
            result = collection.insert_one(data)
            

        return ('inserted successfully')




def delete_item(item_id):
    
    return('in function')
    result = collection.delete_one({"_id": pymongo.ObjectId(item_id)})
    
    if result.deleted_count == 1:
        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'Item deleted successfully'})
        }
    else:
        return {
            'statusCode': 404,
            'body': json.dumps({'message': 'Item not found'})
        }




def build_response(status_code, body):
    return {
        'statusCode': status_code,
        'headers': {
            'Content-Type': 'application/json'
        },
        'body': dumps(body)
    }