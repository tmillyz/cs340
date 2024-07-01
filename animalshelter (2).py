from pymongo import MongoClient
from bson.objectid import ObjectId
import urllib.parse


class AnimalShelter(object):
    """CRUD operations for Animal Collection in MongoDB"""

    def __init__(self, user, password, host, port, db, collection):
        # Initialize Connection
        self.client = MongoClient(f'mongodb://{user}:{password}@{host}:{port}')
        self.database = self.client[db]
        self.collection = self.database[collection]

    # Complete this create method to implement the C in CRUD.
    def create(self, data):
        if data is not None:
            insert_result = self.collection.insert_one(data)  # data should be a dictionary
            return insert_result.acknowledged
        else:
            raise Exception("Nothing to save, because data parameter is empty")

    # Create method to implement the R in CRUD
    def read(self, searchData=None, rescue_type=None):
        projection = {}  # Include all fields by default
        if searchData is not None and '_id' not in searchData:
            projection["_id"] = False  # Exclude _id if not requested in searchData

        if searchData is None:
            searchData = {}

        if rescue_type == 'water_training':
            searchData.update({
                "breed": {"$in": ["Labrador Retriever Mix", "Chesapeake Bay Retriever", "Newfoundland"]},
                "sex_upon_outcome": "Intact Female",
                "age_upon_outcome_in_weeks": {"$gte": 26, "$lte": 156}
            })
        elif rescue_type == 'mountain_wilderness':
            searchData.update({
                "breed": {"$in": ["German Shepherd", "Alaskan Malamute", "Old English Sheepdog", "Siberian Husky", "Rottweiler"]},
                "sex_upon_outcome": "Intact Male"
            })
        elif rescue_type == 'disaster_tracking':
            searchData.update({
                "breed": {"$in": ["Doberman Pinscher", "German Shepherd", "Golden Retriever", "Bloodhound", "Rottweiler"]},
                "sex_upon_outcome": "Intact Male",
                "age_upon_outcome_in_weeks": {"$gte": 26, "$lte": 156}
            })

        data = self.collection.find(searchData, projection)
        return list(data)

    # Create method to implement the U in CRUD
    def update(self, query, update_data):
        if query and update_data:
            update_result = self.collection.update_many(query, {'$set': update_data})
            return update_result.modified_count
        else:
            raise Exception("Update data is empty")

    # Create method to implement the D in CRUD
    def delete(self, query):
        if query:
            delete_result = self.collection.delete_many(query)
            return delete_result.deleted_count
        else:
            raise Exception("Parameter is empty")                                                                      