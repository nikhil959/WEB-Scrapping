import csv
import pymongo
from pymongo import MongoClient
import os

# getting absolute path
cwd = os.path.dirname(__file__)

# delete Existing File to remove duplicates interion
os.remove(cwd+'test.csv') if os.path.exists(cwd+'test.csv') else None

client = MongoClient('mongodb://developer:Internship1234V@tnenggcolleges-shard-00-00.prbcz.mongodb.net:27017,tnenggcolleges-shard-00-01.prbcz.mongodb.net:27017,tnenggcolleges-shard-00-02.prbcz.mongodb.net:27017/TnEnggColleges?ssl=true&replicaSet=atlas-vy8ipk-shard-0&authSource=admin&retryWrites=true&w=majority')
#connection client to connect to MongoDB.
file = open(cwd+'test.csv', 'w', newline ='') 
#opening File

def fetch_data():
   db = client.TnEnggColleges
   collection = db.TnEnggColleges
   pipeline = [
       {
           "$match": {}
       },
       {
           "$project": {
               "college_name": 1,
               "college_code": 1,
               "email": 1,
               "address": 1,
               "pin_code": 1,
               "phone_number": 1,
               "website": 1
           }
       }
   ]
   mongo_result = list(db.TnEnggColleges.aggregate(pipeline))
   # fetching result from mongoDB
   if mongo_result:
       
       header = ['College Name', 'College Code', 'Email', 'Address', 'Pin Code', 'Phone Number', 'Website']
       with file:
           writer = csv.DictWriter(file, fieldnames = header)
           writer.writeheader()
           for item in mongo_result:
               #writting FIle
               writer.writerow({
                    "College Name": item.get("college_name", ""),
                    "College Code": item.get("college_code", ""),
                    "Email": item.get("email", ""),
                    "Address": item.get("address", ""),
                    "Pin Code": item.get("pin_code", ""),
                    "Phone Number": item.get("phone_number", ""),
                    "Website": item.get("website", "")
               })

#function Name
fetch_data()
            


