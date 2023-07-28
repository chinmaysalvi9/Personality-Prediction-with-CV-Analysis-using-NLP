import pymongo
from urllib.parse import quote_plus

client = pymongo.MongoClient(
    f"mongodb+srv://Chinmay:{quote_plus('c5A4nzBfhBonZbnN')}@cluster.hs3fy.mongodb.net/?retryWrites=true&w=majority"
)
database = client["database"]
