# Shopee Market Place Scraper

This project automates the daily scraping of product data from three Shopee marketplaces. It focuses on collecting information about some brands based on their product sales and ratings. The gathered data is exported to a Google Sheet for easy access and analysis.

## Features

- Scrapes product data from three Shopee marketplaces.
- Collects data based on product sales and ratings.
- Schedules daily scraping tasks automatically.
- Exports the final data to a Google Sheet.
- Keeps Google API credentials secure using environment variables.


## Technologies Used
- Python
- Modules: `requests`, `datetime`, `time`, `logging`, `schedule`, `os`, `gspread`, `dotenv`
- Google Sheets API

## Getting Started
### 1. Clone the Repository
```bash
git clone https://github.com/Akichan0201/database_shopee.git
cd database_shopee
```

### 2. Create and activate a virtual environment (optional but recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install the required packages:
```bash
pip install -r requirements.txt
```

### 4. Set up Google Sheets API Credentials:
- Create a project in the [Google Sheets Console](https://console.cloud.google.com/welcome?inv=1&invt=AbyJKw&project=silver-antonym-460214-g3).
- Enable the Google Sheets API for your project.
- Create a service account and download the JSON credentials file.
- Save the credentials file securely and note this path.
- Create a `.env` file in the project root directiory and add the following line:
```bash
GOOGLE_SHEETS_CREDENTIALS_PATH=path/to/your/credentials.json
```
Replace `path/to/your/credentials.json` with the actual path to your credentials file.

### 5. Run the main script
```bash
python main.py
```
This will scrape the data and export it to your scpecified Google Sheet.


## Scheduling Daily Tasks
The project uses the schedule module to automate daily scraping. The main.py script includes a scheduled job that runs the scraping and exporting process every day at a specified time. Ensure that this script is running continuously or set up a system scheduler (like cron on Unix or Task Scheduler on Windows) to execute it daily.

## Security and Privacy
To keep your Google API credentials secure:
- Store th credentials file outside of your version control system.
- Use the `.env` file to reference the credentials path.
- Ensure thet `.env` is listed in your `.gitignore` file to prevent it from being commited.

## Contact
For questions of feedback, please reach out to adzkialma@gmail.com


