# -*- coding: utf-8 -*-
#Plots the number of contributions of the top 50 contributors

import matplotlib.pyplot as plt 
import pprint
import numpy as np
import seaborn 

def get_db(db_name):
    from pymongo import MongoClient
    client = MongoClient('localhost:27017')
    db = client[db_name]
    return db
    
def aggregate(db):
    aggregate_query = [{"$group":{"_id":"$created.user", "count":{"$sum":1}}}, {"$sort":{"count":-1}}, {"$limit":50}]
    return [doc for doc in db.seattle.aggregate(aggregate_query)]

def plot(cursor):
	count_list = []
	for document in cursor:
		count_list.append(document['count'])
	count_array = np.array(count_list)
	x_list = []
	for x in range(50):
		x_list.append(x)
	x_array = np.array(x_list)
	plt.hist2d(x_array, count_array, bins=50)
	plt.xlabel("Users by Number of Contributions")
	plt.ylabel("Number of Contributions")
	plt.title("Influence of Top 50 Contributors")
	plt.show()

if __name__ == '__main__':
    db = get_db('openstreetmap')
    cursor = aggregate(db)
    plot(cursor)