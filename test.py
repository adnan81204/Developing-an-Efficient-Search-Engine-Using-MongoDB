import pymongo

# Connect to MongoDB
def connect_to_mongo():
    client = pymongo.MongoClient("mongodb://localhost:27017/")  # Change this if your MongoDB is hosted elsewhere
    db = client["news_articles_db"]  # The name of the database
    collection = db["articles"]  # The name of the collection
    return collection

# Delete all documents from the collection
def delete_all_articles():
    collection = connect_to_mongo()
    
    # Delete all documents from the collection
    result = collection.delete_many({})
    
    print(f"Deleted {result.deleted_count} articles from the collection.")

# Run the function
if __name__ == "__main__":
    delete_all_articles()
