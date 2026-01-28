import os
import re
import time
import requests
import pymongo
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from datetime import datetime
import tkinter as tk
from tkinter import ttk
from tkinter import simpledialog
import shutil
import json

# MongoDB connection
def connect_to_mongo():
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["news_articles_db"]
    collection = db["articles"]
    return collection

# Function to sanitize filenames
def sanitize_filename(title):
    sanitized_title = re.sub(r'[\\/*?:"<>|]', '_', title)
    sanitized_title = sanitized_title.replace("‘", "_").replace("’", "_")
    return sanitized_title

# Fetch articles from NewsAPI
def fetch_articles_from_api(topic, start_date, end_date, api_key):
    url = f'https://newsapi.org/v2/everything?q={topic}&from={start_date}&to={end_date}&sortBy=publishedAt&apiKey={api_key}'
    response = requests.get(url)
    
    if response.status_code != 200:
        print(f"Error fetching articles: {response.status_code}")
        return []
    
    articles = response.json().get('articles', [])
    print(f"Fetched {len(articles)} articles")
    return articles

# Fetch full article content and save it
def fetch_full_content_and_save(url, title, author, article_folder, date):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3")

    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    
    try:
        time.sleep(5)
        page_content = driver.page_source
        sanitized_title = sanitize_filename(title)
        
        # Saving HTML content
        html_folder = os.path.join(article_folder, "html")
        if not os.path.exists(html_folder):
            os.makedirs(html_folder)
        
        html_filename = f"{sanitized_title}.html"
        html_filepath = os.path.join(html_folder, html_filename)

        with open(html_filepath, "w", encoding="utf-8") as f:
            f.write(page_content)
        
        # Saving metadata
        metadata_folder = os.path.join(article_folder, "metadata")
        if not os.path.exists(metadata_folder):
            os.makedirs(metadata_folder)

        metadata_filename = f"{sanitized_title}.txt"
        metadata_filepath = os.path.join(metadata_folder, metadata_filename)
        
        with open(metadata_filepath, "w", encoding="utf-8") as f:
            f.write(f"Title: {title}\n")
            f.write(f"URL: {url}\n")
            f.write(f"Author: {author if author else 'Author not found'}\n")
            f.write(f"Date: {date}\n")  # Adding the date to metadata

        print(f"Saved: {title}")
    except Exception as e:
        print(f"Error fetching the content for {title}: {e}")
    finally:
        driver.quit()


# Save articles to MongoDB
def save_articles_to_db(articles):
    collection = connect_to_mongo()
    for article in articles[:5]:
        title = article['title']
        author = article.get('author', "Unknown")
        url = article['url']
        date = article['publishedAt']  # Getting the date from the article
        sanitized_title = sanitize_filename(title)
        
        # Inserting article data into MongoDB with date included
        article_data = {
            "title": title,
            "author": author,
            "url": url,
            "date": date,  # Saving the date to MongoDB
            "html_file": f"html/{sanitized_title}.html"
        }
        
        collection.insert_one(article_data)
        print(f"Saved to DB: {title}")


# Update UI with articles
def update_ui_with_articles(articles, treeview):
    for article in articles:
        treeview.insert("", "end", values=(article['title'], article.get('author', "Unknown"), article['url'], article['publishedAt']))

# Save articles to MongoDB
def save_articles():
    folder = r"D:\srinidhi\fds\articles_temp"  # Updated to your desired folder location
    if not os.path.exists(folder):
        print("No articles folder found.")
        return

    # MongoDB connection
    collection = connect_to_mongo()

    # Loop through each article folder in articles_temp
    for article_folder in os.listdir(folder):
        article_path = os.path.join(folder, article_folder)
        if os.path.isdir(article_path):
            metadata_filepath = os.path.join(article_path, "metadata", f"{article_folder}.txt")
            html_filepath = os.path.join(article_path, "html", f"{article_folder}.html")

            if os.path.exists(metadata_filepath) and os.path.exists(html_filepath):
                try:
                    with open(metadata_filepath, "r", encoding="utf-8") as f:
                        metadata = f.readlines()

                    # Ensure metadata contains at least 3 expected fields
                    title, author, date, url = None, None, None, None

                    # Extract title
                    for line in metadata:
                        if line.startswith("Title:"):
                            title = line.split("Title:")[1].strip()
                            break  # Stop after finding the title

                    # Extract URL
                    for line in metadata:
                        if line.startswith("URL:"):
                            url = line.split("URL:")[1].strip()
                            break  # Stop after finding the URL

                    # Extract author (handle potential issues with "author" being listed as a field)
                    for line in metadata:
                        if line.startswith("Author:"):
                            author = line.split("Author:")[1].strip()
                            break  # Stop after finding the author

                    # If any field is missing, set a default value
                    if not title:
                        title = "No title available"
                    if not author:
                        author = "Unknown author"
                    if not date:
                        date = "Unknown date"
                    if not url:
                        url = "Unknown URL"

                    # Insert the article data into MongoDB
                    article_data = {
                        "title": title,
                        "author": author,
                        "url": url,
                        "date": date,
                        "html_file": html_filepath
                    }
                    collection.insert_one(article_data)
                    print(f"Saved: {title}")
                except Exception as e:
                    print(f"Error reading metadata for {article_folder}: {e}")
            else:
                print(f"Metadata or HTML not found for {article_folder}")


# Validate date format function
def validate_date(date_string):
    try:
        datetime.strptime(date_string, "%Y-%m-%d")
        return True
    except ValueError:
        return False

def main():
    def search_articles():
        topic = topic_entry.get()
        start_date = start_date_entry.get()
        end_date = end_date_entry.get()

        # Validate date inputs
        if not validate_date(start_date) or not validate_date(end_date):
            print("Invalid date format. Please use YYYY-MM-DD.")
            return

        api_key = "461fa46e66d64182b3a279f64700dbcc"  # Replace with your NewsAPI key

        # Fetch only 10 articles based on the topic and date range
        articles = fetch_articles_from_api(topic, start_date, end_date, api_key)
        articles_to_scrape = articles[:5]  # Limit to the first 10 articles for scraping

        if not articles_to_scrape:
            print("No articles found.")
            return
        
        # Save articles to a folder (if user clicks save)
        folder = "articles_temp"
        if not os.path.exists(folder):
            os.makedirs(folder)

        # Scrape only the first 10 articles
        for article in articles_to_scrape:  
            title = article['title']
            url = article['url']
            author = article.get('author', "Unknown")
            article_folder = os.path.join(folder, sanitize_filename(title))
            if not os.path.exists(article_folder):
                os.makedirs(article_folder)

            fetch_full_content_and_save(url, title, author, article_folder, article['publishedAt'])
        
        # Save articles to MongoDB (only 10)
        save_articles_to_db(articles_to_scrape)

        # Update the treeview with the articles
        update_ui_with_articles(articles_to_scrape, treeview)

    # Tkinter UI setup
    root = tk.Tk()
    root.title("News Article Fetcher")

    # Search UI elements
    search_frame = tk.Frame(root)
    search_frame.pack(pady=20)

    topic_label = tk.Label(search_frame, text="Topic:")
    topic_label.grid(row=0, column=0)
    topic_entry = tk.Entry(search_frame)
    topic_entry.grid(row=0, column=1)

    start_date_label = tk.Label(search_frame, text="Start Date (YYYY-MM-DD):")
    start_date_label.grid(row=1, column=0)
    start_date_entry = tk.Entry(search_frame)
    start_date_entry.grid(row=1, column=1)

    end_date_label = tk.Label(search_frame, text="End Date (YYYY-MM-DD):")
    end_date_label.grid(row=2, column=0)
    end_date_entry = tk.Entry(search_frame)
    end_date_entry.grid(row=2, column=1)

    search_button = tk.Button(search_frame, text="Search", command=search_articles)
    search_button.grid(row=3, column=0, columnspan=2)

    # Articles list UI elements
    treeview_frame = tk.Frame(root)
    treeview_frame.pack(pady=20)

    columns = ("Title", "Author", "URL", "Published At")
    treeview = ttk.Treeview(treeview_frame, columns=columns, show="headings")
    treeview.pack(fill="both", expand=True)

    for col in columns:
        treeview.heading(col, text=col)

    root.mainloop()

if __name__ == "__main__":
    main()
