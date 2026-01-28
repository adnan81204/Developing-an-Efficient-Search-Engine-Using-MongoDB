# Developing an Efficient Search Engine Using MongoDB

A **Big Data–oriented Search Engine** built using **MongoDB** to efficiently store, index, and retrieve large volumes of **structured and unstructured data**.  
The system supports **fast full-text search**, **query caching**, and **scalable data management**, making it suitable for real-time and historical data analysis.

---

## Overview

With the rapid growth of big data, traditional relational databases struggle to handle **high-volume, heterogeneous datasets**.  
This project leverages **MongoDB’s document-oriented architecture** to build a scalable and high-performance search engine capable of:

- Handling unstructured data  
- Performing fast text-based searches  
- Supporting real-time and historical queries  
- Improving query performance using indexing and caching  

---

## Key Features

- Full-text search on documents and articles  
- Fast data retrieval using MongoDB indexing  
- Query caching for repeated searches  
- Support for multiple data sources:
  - News articles  
  - Names & metadata  
  - User-uploaded documents (PDF, DOCX, TXT, Images)  
- Highlighting matched query terms  
- Modular and scalable architecture  

---

## Tech Stack

| Category        | Technology                      |
|-----------------|----------------------------------|
| Database        | MongoDB                          |
| Backend         | Python                           |
| GUI             | Tkinter                          |
| Text Extraction | OCR / Text parsing libraries     |
| Indexing        | MongoDB Text & Compound Indexes  |
| Caching         | In-memory query caching          |

---

## System Architecture

User
│
▼
Tkinter GUI
│
▼
Search Controller
│
├── Main Search Module
│ ├── News Articles DB
│ └── Names DB
│
├── Self Search Module
│ └── Files DB (PDF, DOCX, TXT, Images)
│
▼
MongoDB Database
│
├── Indexed Collections
├── Cached Queries
│
▼
Search Results Display

---

##  Methodology

### Data Acquisition

- News articles and metadata stored in MongoDB  
- User-uploaded files parsed and stored with extracted text  

### Data Modeling

- Separate MongoDB collections for:
  - Names Database  
  - News Articles Database  
  - Files Database  
- Indexes created on frequently queried fields  

###  Search Functionality

- Keyword-based querying  
- Date-range and topic-based filtering  
- Cached result reuse for faster execution  

###  Caching Mechanism

- Query results cached using a composite key:
<query + document type + date range>

- Reduces redundant database hits  

###  User Interface

- Tkinter-based GUI  
- Tab-based layout:
- Main Search  
- Self Search  
- Results displayed using Treeview tables  

---

## Installation & Setup

### Step 1: Install MongoDB

- Download and install MongoDB from:
https://www.mongodb.com/try/download/community

### Step 2: Install Python Dependencies

pip install pymongo tkinter pillow pytesseract

### Step 3: Start MongoDB Server

mongod

### Step 4: Run the Application

python main.py

---

## Usage
- Launch the application
- Choose Main Search or Self Search
- Enter a keyword or upload a document
- Apply filters (date, topic, type)
- View highlighted and structured results

## Results
- Efficient retrieval of real-time and historical data
- Improved query execution time using indexing
- Reliable caching mechanism for repeated searches
- Well-structured data storage and retrieval

## Limitations
- GUI limited to desktop (Tkinter-based)
- Advanced NLP ranking not implemented
- No distributed framework integration (yet)

## Future Enhancements
- Integration with Hadoop / Spark for large-scale processing
- Machine learning–based query prediction
- Web-based UI using Flask or React
- Semantic search and relevance ranking
- Real-time streaming data ingestion

## Authors
Rushank Tripathi

Aryan Kumar Sah

Shaik Adnan Tousef

Department of Computer Science and Engineering
Amrita School of Computing, Bengaluru

 ## License
This project is developed for academic and educational purposes.
All rights reserved to the authors.

***Built for Big Data. Designed for Performance.***
