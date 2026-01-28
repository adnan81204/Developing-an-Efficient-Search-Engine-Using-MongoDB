import pymongo
from pprint import pprint

# Connect to MongoDB
def connect_to_mongo():
    client = pymongo.MongoClient("mongodb://localhost:27017/")  # Change this if your MongoDB is hosted elsewhere
    db = client["news_articles_db"]  # The name of the database
    collection = db["articles"]  # The name of the collection
    return collection

# Fetch and display all documents from the collection
def fetch_and_display_articles():
    collection = connect_to_mongo()
    
    # Fetch all articles
    articles = collection.find()
    
    # Print articles in a readable format
    print("Displaying all articles in the database:\n")
    for article in articles:
        pprint(article)  # Pretty print each document

# Run the function
if __name__ == "__main__":
    fetch_and_display_articles()
