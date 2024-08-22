from datetime import datetime
from pymongo import MongoClient
from chanblockweb.settings.base import env


import os

class AssetDBManager:
    def __init__(self):
        """
        Initializes the AssetDBManager with a MongoDB database instance.
        """
        # Connection to the MongoDB instance
        # client = MongoClient(os.getenv('MONGOATLAS_USER2'))
        client = MongoClient(env('MONGOATLAS_USER'))
        db = client.chanblock
        self.assetsdb = db.assets  # Connection to the 'assets' collection
       
    
    def find_by_date(self, date):
        """
        Finds assets by a given date.
        :param date: Date to search for
        :return: List of assets for the given date
        """
        return list(self.assetsdb.find({'date': date}, {"_id": 0}))

    def find_last_record_date(self):
        """
        Finds the date of the last record in the assets database.
        :return: Date of the last record
        """
        last_record = self.assetsdb.find({}, {"_id": 0, "date": 1}).sort("_id", -1).limit(1)
        return list(last_record)

    def find_asset_by_symbol(self, symbol):
        detail = list(self.assetsdb.find({"symbol": symbol}).limit(1))
        listMetric = detail[0]
        return listMetric
    
    def find_latest_profile(self):
        client = MongoClient(os.getenv('MONGOATLAS_USER2'))
        db = client.chancblock
        collection = db.profile
        profile = collection.find({}, {"_id": 0, "timestamp": 0}).sort("_id", -1).limit(1)
        return profile
      
    def find_latest_symbols(self):
        """
        Finds the latest symbols from the 'tickers' collection.
        :return: The latest symbols
        """
        return self.assetsdb.tickers.find({}, {"_id": 0, "symbol": 0}).sort("_id", -1).limit(1)


class ProfileManager():
    def __init__(self):
        """
        Initializes the AssetDBManager with a MongoDB database instance.
        """
        # Connection to the MongoDB instance
        client = MongoClient(os.getenv('MONGOATLAS_USER2'))
        db = client.chancblock
        self.profiledb = db.profile  # Connection to the 'profile' collection
    
    def find_latest_profile(self):
        profile = self.profiledb.find({}, {"_id": 0, "timestamp": 0}).sort("_id", -1).limit(1)
        return profile
    
class TickersManager():
     def __init__(self):
        """
        Initializes the AssetDBManager with a MongoDB database instance.
        """
        # Connection to the MongoDB instance
        client = MongoClient(os.getenv('MONGOATLAS_USER2'))
        db = client.chancblock
        self.tickersdb = db.tickers  # Connection to the 'profile' collection
     
     def find_latest_symbols(self):
        """
        Finds the latest symbols from the 'tickers' collection.
        :return: The latest symbols
        """
        return self.tickersdb.find({}, {"_id": 0, "symbol": 0}).sort("_id", -1).limit(1)