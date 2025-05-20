# Shopee Daily Sales Scraper

A Python-based scraper that collects product sales data from Shopee. It tracks sold counts daily and organizes data by rating, brand, and date. All data is stored in a local SQLite database for easy access and analysis.

## STAR Summary

**Situation:** Shopee does not offer direct access to structured daily sales data, making it difficult to monitor product trends over time.

**Task:** Develop an automated script that scrapes product information daily and saves it into a database for long-term tracking and analysis.

**Action:**  
- Collected product data using the Shopee public API through the `requests` module  
- Processed and cleaned data with `pandas`, `datetime`, and `numpy`  
- Stored daily product snapshots in an SQLite database  
- Used the `schedule` module to automate daily scraping  
- Added logging to monitor and debug the scraping process

**Result:**  
A functioning daily scraper that saves Shopee product sales data based on rating, brand, and date. Enables structured tracking and future analysis through the database.

## Features

- Tracks number of items sold on Shopee by day
- Filters and organizes data by rating, brand, and date
- Saves data in `shopee.db` using SQLite
- Automates scraping with scheduling
- Logs scraping activity for transparency

## How to Use

### 1. Clone the Repository

```bash
git clone https://github.com/Akichan0201/database_shopee.git
cd database_shopee
```

### 2. install dependencies
```bash
pip install requests pandas numpy schedule
```

### 3. Run the Script
```bash
python main.py
```
You can also schedule it to run in the background using a task scheduler or a background process.

## Output
- SQLite database shopee.db with daily records of product sales.
- Tables include product name, brand, rating, sold count, and date, but you can also keep all the data you got or just choose what you need.

---

Let me know if you'd like help adding visualization tools, database export to CSV, or a small dashboard interface.
