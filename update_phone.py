# -*- coding: utf-8 -*-
#Updates phone numbers in mongoDB database to format XXX-XXX-XXXX or 1-XXX-XXX-XXXX
#invalid phone numbers are changed to "FIXME"
import pprint
import re

def get_db(db_name):
    from pymongo import MongoClient
    client = MongoClient('localhost:27017')
    db = client[db_name]
    return db

def update_phone(phone_number):
	p = re.compile('\D+')
	updated_phone = re.sub(p, "", phone_number)
	if len(updated_phone) == 11:
		final_phone = updated_phone[0] + "-" + updated_phone[1:4] + "-" + updated_phone[4:7] + "-" + updated_phone[7:]
		return final_phone
	elif len(updated_phone) == 10:
		final_phone = updated_phone[0:3] + "-" + updated_phone[3:6] + "-" + updated_phone[6:]
		return final_phone
	else:
		return "FIXME"

if __name__ == '__main__':
    db = get_db('openstreetmap')
    x = db.seattle.find({"phone" : {"$exists" : 1}})
    for document in x:
    	document["phone"] = update_phone(document["phone"])
    	db.seattle.update({"_id" : document["_id"]}, document)



