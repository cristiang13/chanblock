from datetime import datetime
from pymongo import MongoClient
from chanblockweb.settings.base import env

import os

class CoinmetricDBManager:
    def __init__(self):
        """
        Initializes the GraphicDBManager with a MongoDB database instance.
        """
        # Connection to the MongoDB instance
        client = MongoClient(env('MONGOATLAS_USER1'))

        self.db = client.coinmetrics  # Connection to the 'coinmetrics' database
    
    def get_price(self, collection, field, additional_field=None):
        """
        Retrieves data for a given field from the specified collection.

        Args:
        collection (str): The collection to query.
        field (str): The field for which to retrieve data.
        additional_field (str, optional): An additional field to include in the query, if required.

        Returns:
        list: A list of documents containing the specified fields.
        """
     
        query = {field: {"$exists": True}}
        projection = {"_id": 0, "time": 1, field: 1}
        
        if additional_field:
            projection[additional_field] = 1
      
        return list(self.db[collection].find(query, projection).sort("time", 1))
    
    def get_values(self, collection, field, additional_field=None):
        """
        Retrieves data for a given field from the specified collection. If the field is an array,
        retrieves documents where the field contains any of the values in the array.
        Args:
            collection (str): The collection to query.
            field (str or list): The field for which to retrieve data, or a list of values to match in the field.
            additional_field (str, optional): An additional field to include in the query, if required.
        Returns:
            list: A list of documents containing the specified fields.
        """

        
        # Adjust query based on whether field is a string or a list
        if isinstance(field, list):
            query = {"$or": [{f: {"$exists": True}} for f in field]}
            projection = {"_id": 0, "time": 1}
            for f in field:
                projection[f] = 1
        else:
            query = {field: {"$exists": True}}
            projection = {"_id": 0, "time": 1, field: 1}
        
        if additional_field:
            projection[additional_field] = 1
        
        return list(self.db[collection].find(query, projection).sort("time", 1))
