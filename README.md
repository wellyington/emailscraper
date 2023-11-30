# Email Scraper App

## Overview

This Python script is designed to scrape email addresses from websites based on a user-provided search term. It utilizes the Google Search API to gather a specified number of URLs related to the search term and then scans a specified number of pages from each URL to extract email addresses. The extracted emails are stored in a SQLite database and exported to an Excel file for further analysis.

## Features

* Google Search integration for collecting relevant URLs.
* Web scraping to extract email addresses from the specified web pages.
* Storage of collected emails in a SQLite database.
* Deletion of emails containing specified "bad words" to filter out irrelevant or unwanted results.
* Export of unique and valid email addresses to an Excel file.

## Prerequisites

Before running the script, make sure you have the following dependencies installed:

* `BeautifulSoup`: HTML parsing library
* `requests`: HTTP library for making requests to websites
* `googlesearch-python`: Google Search API
* `xlsxwriter`: Library for creating Excel files

Install these dependencies using the following:

`pip install beautifulsoup4 requests googlesearch-python xlsxwriter`

## Usage

1. Clone the repository:

   `git clone https://github.com/wellyington/emailscraper.git`

2.  Create a virtual environment (optional but recommended):

    `cd emailscraper`
   
    `python3 -m venv venv`
   
    `source venv/bin/activate  # On Windows, use venv\Scripts\activate`

3. Install the required packages:

   `pip install -r requirements.txt`

4. Run the script:

   `python scraper.py`

Follow the prompts to input the search term, number of URL results, and number of pages to scan. The script will then collect emails, filter out invalid ones, and export the results to an Excel file.

## Configuration

The script uses a configuration file (config.py) to specify "bad words" that will be used to filter out unwanted emails. Ensure this file is configured to meet your needs.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

