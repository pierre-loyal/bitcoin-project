## Bitcoin Data Pipelines

### This repository contains two ETL pipelines:

Financial Times Article Scraper: This pipeline scrapes Bitcoin-related articles from the Financial Times website using BeautifulSoup, formats publication dates, and stores the article titles and dates in an SQLite database, sorted in descending order by date.

Bitcoin Price API Pipeline: This pipeline retrieves daily Bitcoin price data from the Alpha Vantage API, processes the data to include open, high, low, close, and volume metrics, and stores it in an SQLite database for further analysis.
