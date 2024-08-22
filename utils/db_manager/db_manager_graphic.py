from datetime import datetime
from pymongo import MongoClient
import os

class GraphicDBManager:
    def __init__(self):
        """
        Initializes the GraphicDBManager with a MongoDB database instance.
        """
        # Connection to the MongoDB instance
        client = MongoClient(os.getenv('MONGOATLAS_USER2'))
        db = client.chanblock
        self.assetsdb = db.assets  # Connection to the 'assets' collection