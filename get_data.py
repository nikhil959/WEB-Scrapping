from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import re
import json
import pymongo
from pymongo import MongoClient
from datetime import datetime
from urllib.error import HTTPError
from urllib.error import URLError
import random
from fake_useragent import UserAgent
import time
import urllib
# Modules imported

client = MongoClient('mongodb://developer:Internship1234V@tnenggcolleges-shard-00-00.prbcz.mongodb.net:27017,tnenggcolleges-shard-00-01.prbcz.mongodb.net:27017,tnenggcolleges-shard-00-02.prbcz.mongodb.net:27017/TnEnggColleges?ssl=true&replicaSet=atlas-vy8ipk-shard-0&authSource=admin&retryWrites=true&w=majority')
#connection client to connect to MongoDB.

def insert_data(data):
    """ This function to insert and update the database.
    """
    try:
        #Naming the DB
        db = client.TnEnggColleges  
        #Naming the COllection.
        collection = db.TnEnggColleges
        #the time of storing into database
        data["created_time"] = datetime.utcnow()
        #adding extra keys.
        data["target"] = "Anna University"
        #checking the condition if it founds insert or else update
        if db.TnEnggColleges.find_one({"college_code": data.get("college_code")}):
            db.TnEnggColleges.update_one({"college_code": data.get("college_code")}, {"$set": data})
            print({"status_id": 1, "response": "updated Successfully"})
        else:
            result = db.TnEnggColleges.insert_one(data).inserted_id
            if not result:
                return {"status_id": 0, "response":"Failed adding data"}
        #closeing the connection
        client.close()
        return {"status_id": 1, "response": "inserted Successfully"}
    except Exception as e:
        pass


def get_data_url(no1, no2):
    # no1 is the number which to be started and no2 is the number to end.
    for i in range(no1, no2+1):
        if i%10 == 0:
            # this is for to sleep after every 10 records for 10 seconds to avoid connection timed out error from the website.
            time.sleep(10)
        # this is to know how many records have successfully completed.
        print(i)
        try:
            #connecting to website using bs4
            req = urllib.request.Request(
            "https://tneacounseling.com/engineeringCollege-details?code="+ str(i), 
            data=None, 
            headers={
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
            }
            )
            html = urllib.request.urlopen(req)
            time.sleep(1)
        except HTTPError as e:
            pass
        try:
            bs = BeautifulSoup(html.read(), 'html.parser')
        except AttributeError as e:
            pass
        try:
            # from here data generation from the website page starts.
            data = {}
            if bs.find('iframe'):
                if bs.find('iframe').get('src'):
                    data["location"] = bs.find('iframe')['src']
            else:
                data["location"] = ""
            data["academic_fee_details"] = {}
            data["hostel_details"] = {}
            data["transport_details"] = {}
            data["other_details"] = {}
            for item in bs.find_all('tr'):
                find_text = item.find_all('td')[0].get_text()
                if find_text == "College Name":
                    data["college_name"] = item.find_all('td')[-1].get_text()
                    data.update(data)
                if find_text == "College Code":
                    data["college_code"] = item.find_all('td')[-1].get_text()
                    data.update(data)
                if find_text == "Address":
                    data["address"] = item.find_all('td')[-1].get_text()
                    data["pincode"] = re.search(r'.*(\d{6}(\-\d{4})?)$', item.find_all('td')[-1].get_text()).group(1)
                    data.update(data)
                if find_text == "Nearest Railway Station":
                    data["nearest_railway_station"] = item.find_all('td')[-1].get_text()
                    data.update(data)
                if find_text == "Phone":
                    data["phone_number"] = item.find_all('td')[-1].get_text()
                    data.update(data)
                if find_text == "Fax":
                    data["fax"] = item.find_all('td')[-1].get_text()
                    data.update(data)
                if find_text == "Email":
                    data["email"] = item.find_all('td')[-1].get_text()
                    data.update(data)
                if find_text == "Website":
                    data["website"] = item.find_all('td')[-1].get_text()
                    data.update(data)
                if find_text == "UG Courses":
                    data["ug_courses"] = [i.strip() for i in item.find_all('td')[-1].get_text().split('-')]
                    data.update(data)
                if find_text == "PG Courses":
                    if item.find_all('td')[-1].get_text():
                        data["pg_courses"] = [i.strip() for i in item.find_all('td')[-1].get_text().split('-')]
                    else:
                        data["pg_courses"] = ""
                    data.update(data)
                if find_text == "Tuition Fees":
                    data["academic_fee_details"]["tuition_fees"] = item.find_all('td')[-1].get_text()
                    data.update(data)
                if find_text == "Hostel For Boys":
                    data["hostel_details"]["hostel_for_boys"] = item.find_all('td')[2].get_text()
                    data["hostel_details"][item.find_all('td')[3].get_text().replace(".","_")] = item.find_all('td')[5].get_text()
                    data.update(data)
                if find_text == "Mess Bill(Rs.Per Month or Per Year)":
                    data["hostel_details"][item.find_all('td')[0].get_text().replace(".","_")] = item.find_all('td')[2].get_text()
                    data["hostel_details"][item.find_all('td')[3].get_text().replace(".","_")] = item.find_all('td')[5].get_text()
                    data.update(data)
                if find_text == "Electricity Charges(Rs.Per Month or Per Year)":
                    data["hostel_details"][item.find_all('td')[0].get_text().replace(".","_")] = item.find_all('td')[2].get_text()
                    data["hostel_details"][item.find_all('td')[3].get_text().replace(".","_")] = item.find_all('td')[5].get_text()
                    data.update(data)
                if find_text == "Establishment Charges(Rs.Per Month or Per Year)":
                    data["hostel_details"][item.find_all('td')[0].get_text().replace(".","_")] = item.find_all('td')[2].get_text()
                    data["hostel_details"][item.find_all('td')[3].get_text().replace(".","_")] = item.find_all('td')[5].get_text()
                    data.update(data)
                if find_text == "Transport Available":
                    data["transport_details"][item.find_all('td')[0].get_text().replace(".","_")] = item.find_all('td')[2].get_text()
                    data["transport_details"][item.find_all('td')[3].get_text().replace(".","_")] = item.find_all('td')[5].get_text()
                    data.update(data)
                if find_text == "Minimum Charge(Rs.Per Month or Per Year)":
                    data["transport_details"][item.find_all('td')[0].get_text().replace(".","_")] = item.find_all('td')[2].get_text()
                    data["transport_details"][item.find_all('td')[3].get_text().replace(".","_")] = item.find_all('td')[5].get_text()
                    data.update(data)
                if find_text == "Library Facility":
                    data["other_details"][item.find_all('td')[0].get_text().replace(".","_")] = item.find_all('td')[2].get_text()
                    data["other_details"][item.find_all('td')[3].get_text().replace(".","_")] = item.find_all('td')[5].get_text()
                    data.update(data)
                if find_text == "Sports Facility":
                    data["other_details"][item.find_all('td')[0].get_text().replace(".","_")] = item.find_all('td')[2].get_text()
                    data["other_details"][item.find_all('td')[3].get_text().replace(".","_")] = item.find_all('td')[5].get_text()
                    data.update(data)
                if find_text == "Banking Facility":
                    data["other_details"][item.find_all('td')[0].get_text().replace(".","_")] = item.find_all('td')[2].get_text()
                    data["other_details"][item.find_all('td')[3].get_text().replace(".","_")] = item.find_all('td')[5].get_text()
                    data.update(data)
            #if data not found skip .
            if not bs.find('iframe') and not data.get("academic_fee_details") and not data.get("hostel_details") and not data.get("transport_details") and not data.get("other_details"):
                continue
            # passing data to update or insert to database
            result = insert_data(data)
            if not result.get("status_id"):
                return result
        except Exception as e:
            print(e)
            pass
    return {"status_id": 1, "response": "college code entered Successfully"}

print("Enter the starting Number")    
number1 = int(input())
print("Enter the Ending Number")
number2 = int(input())
# Calling Function.
print(get_data_url(number1, number2))
    