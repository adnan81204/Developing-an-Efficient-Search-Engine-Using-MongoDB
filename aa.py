import pymongo
import re
import webbrowser
from pprint import pprint

# Connect to MongoDB
def connect_to_mongo():
    client = pymongo.MongoClient("mongodb://localhost:27017/")  # Change this if your MongoDB is hosted elsewhere
    db = client["news_articles_db"]  # The name of the database
    collection = db["articles"]  # The name of the collection
    return collection

# Escape special characters for URL query
def escape_special_characters(text):
    return re.escape(text)  # This will escape all special regex characters in the string

# Search for articles with title, date, url, and author filters
def search_articles(title_query=None, date_query=None, url_query=None, author_query=None):
    collection = connect_to_mongo()

    # Initialize the query as an empty dictionary
    query = {}

    # Title search (case-insensitive)
    if title_query:
        query["title"] = {"$regex": title_query, "$options": "i"}  # Case-insensitive search for title

    # Date search (exact match, regex for start of date)
    if date_query and date_query.lower() != "skip":
        query["date"] = {"$regex": f"^{date_query}", "$options": "i"}  # Case-insensitive regex match for date (start of date)

    # URL search (escape special characters)
    if url_query and url_query.lower() != "skip":
        query["url"] = {"$regex": escape_special_characters(url_query), "$options": "i"}  # Escape URL and perform regex search

    # Author search (case-insensitive)
    if author_query and author_query.lower() != "skip":
        query["author"] = {"$regex": author_query, "$options": "i"}  # Case-insensitive search for author

    # Perform the query
    results = collection.find(query)
    
    # Convert results to a list and get the count
    results_list = list(results)

    # Save the search results to the cache (overwrite previous search)
    save_previous_search_results(results_list)
    
    return results_list

# Save the previous search results to a file (overwrite the file every time)
def save_previous_search_results(results_list):
    with open("previous_search_results.txt", "w") as file:
        # Write the search results to the file
        for result in results_list:
            file.write(f"Title: {result['title']}\n")
            file.write(f"Author: {result['author']}\n")
            file.write(f"Date: {result['date']}\n")
            file.write(f"URL: {result['url']}\n")
            file.write("\n")  # Add a new line between results

# Load the previous search results from the cache file
def load_previous_search_results():
    try:
        with open("previous_search_results.txt", "r") as file:
            content = file.read()
            return content
    except FileNotFoundError:
        return "No previous search results found."

# Automatically open the URL in the default web browser
def open_urls(results_list):
    for result in results_list:
        webbrowser.open(result['url'])  # Open each URL in the default browser

# Run the function
if __name__ == "__main__":
    # Show previous search results
    print("Previous Search Results:\n")
    print(load_previous_search_results())

    # Get user input for a new search
    title = input("Enter title query (e.g., 'India') or press enter to skip: ").strip()
    date = input("Enter date query (e.g., '2024-01-01') or press enter to skip: ").strip()
    url = input("Enter URL query (e.g., 'sports.ndtv.com') or press enter to skip: ").strip()
    author = input("Enter author query (e.g., 'Uma Sudhir') or press enter to skip: ").strip()
    
    # Call the search function with user input
    results = search_articles(
        title_query=title if title.lower() != "skip" else None,
        date_query=date if date.lower() != "skip" else None,
        url_query=url if url.lower() != "skip" else None,
        author_query=author if author.lower() != "skip" else None
    )

    # Show the new search results
    print(f"Found {len(results)} result(s):\n")
    pprint(results)  # Pretty print all the matching documents

    # Open the URLs of the results in the default web browser
    open_urls(results)
