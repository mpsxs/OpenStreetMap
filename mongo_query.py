# -*- coding: utf-8 -*-
#Includes all complex queries used in analysis of OpenStreetMap data
import pprint

def get_db(db_name):
    from pymongo import MongoClient
    client = MongoClient('localhost:27017')
    db = client[db_name]
    return db

#Exploratory queries used for checking for types of inconsistencies within dataset
def query():
    query1 = {"address" : {"$exists" : 1}}
    projection1 = {"address" : "$address"}
    query2 = {"phone" : {"$exists" : 1}}
    projection2 = {"phone" : "$phone"}
    #change return values to access different queries
    return query1, projection1

def aggregate(db):
    #top 10 amenities
    aggregate1 = [{"$match":{"amenity":{"$exists":1}}}, {"$group":{"_id":"$amenity", "count":{"$sum":1}}}, {"$sort" :{"count":-1}}, {"$limit":10}]
    #top 10 restaurants
    aggregate2 = [{"$match":{"amenity":{"$exists":1}, "amenity":"restaurant"}}, {"$group":{"_id":"$cuisine", "count":{"$sum":1}}}, {"$sort":{"count":-1}}, {"$limit":10}]
    #top 10 places
    aggregate3 = [{"$match":{"place":{"$exists":1}}}, {"$group": {"_id":"$place", "count":{"$sum":1}}}, {"$sort" :{"count":-1}}, {"$limit":10}]
    #top 10 natural features
    aggregate4 = [{"$match":{"natural":{"$exists":1}}}, {"$group":{"_id":"$natural", "count":{"$sum":1}}}, {"$sort":{"count":-1}}, {"$limit":10}]
    #top 10 man_made features
    aggregate5 = [{"$match":{"man_made":{"$exists":1}}}, {"$group":{"_id":"$man_made", "count":{"$sum":1}}}, {"$sort":{"count":-1}}, {"$limit":10}]
    #number of contributors with 1 contribution
    aggregate6 = [{"$group":{"_id":"$created.user", "count":{"$sum":1}}}, {"$group":{"_id":"$count", "num_users":{"$sum":1}}}, {"$sort":{"_id":1}}, {"$limit":1}]
    #number of contributions for the top 100 contributors
    aggregate7 = [{"$group":{"_id":"$created.user", "count":{"$sum":1}}}, {"$sort":{"count":-1}}, {"$limit":100}]
    #change return_aggregate value to access different results 
    return_aggregate = aggregate1
    return [doc for doc in db.seattle.aggregate(return_aggregate)]

if __name__ == '__main__':
    db = get_db('openstreetmap')

    #change to True to run Query()
    if False:
        query, projection = query()
        result = db.seattle.find(query, projection)
        #change range value to limit number of results
        for counter in range(100):
            pprint.pprint(result[counter])

    #change to True to run Aggregate()
    if False:
        aggregate_result = aggregate(db)
        pprint.pprint(aggregate_result)


