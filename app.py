from flask import Flask,request
from pymongo import MongoClient
from config import DB_NAME,MONGO_SERVER,MONGO_PORT,MONGO_COLLECTION

app = Flask(__name__)
client = MongoClient(MONGO_SERVER, MONGO_PORT)          # Initializing mongo client
mongo_Collection = client[DB_NAME][MONGO_COLLECTION]    # Creating the mongo database collection

@app.route('/updateRecord',methods=['POST'])
def update_record():
    # This is the Flask POST request method which will be used to update the taskID record status in 
    # the database
    
    if request.json:
        if 'taskID' in request.json and 'status' in request.json:
            mongo_Collection.update({'taskID':request.json['taskID']},{'$set':{'status':request.json['status']}},upsert = True)
            return { 'statusCode': 200, 'body': 'Data Insertion Success!!!' }
        else: return { 'statusCode': 500, 'body': 'Check and Send TaskID and Status.' } 
    else: return { 'statusCode': 500, 'body': 'Send the request in Proper JSON Format.' }
    
@app.route('/getRecord',methods=['POST'])
def get_record():
    # This is the Flask POST request method which will be used to return the current status of the taskID
    # in the database. It will take taskID as an input to return the current sttaus of the task
     
    if request.json:
        if 'taskID' in request.json:
            obj = mongo_Collection.find_one({'taskID':request.json['taskID']})
            if obj:  return { 'statusCode': 200, 'body': obj }
            else: return { 'statusCode': 200, 'body': 'TaskID not Found' }
        else: return { 'statusCode': 500, 'body': 'Check and Send TaskID' } 
    else: return { 'statusCode': 500, 'body': 'Send the request in Proper JSON Format.' }

if __name__=='__main__':
    app.run(debug=True,host='localhost',port='7004')
