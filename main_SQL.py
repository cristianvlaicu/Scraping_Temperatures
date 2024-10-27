import requests
import selectorlib
import sqlite3

from datetime import datetime

# Connect to the SQLite database
connection = sqlite3.connect("data.db")

# Define the URL to scrape and the headers to use in the request
URL = "http://programmer100.pythonanywhere.com/"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}


def scrape(url):
    """Scrape the page source from the given URL."""
    response = requests.get(url, headers=HEADERS)  # Send a GET request with the specified headers
    source = response.text  # Get the HTML content of the page
    return source


def extract(source):
    """Extract the temperature value from the HTML source using selectorlib."""
    extractor = selectorlib.Extractor.from_yaml_file("extract.yaml")  # Load the extraction rules from a YAML file
    value = extractor.extract(source)["tours"]  # Extract the value using the rules
    return value


def store(extracted):
    """Store the extracted temperature value and the current timestamp in the database."""
    now = datetime.now().strftime("%y-%m-%d-%H-%M-%S")  # Get the current timestamp
    cursor = connection.cursor()  # Create a database cursor
    cursor.execute("INSERT INTO temperatures VALUES(?, ?)", (now, extracted))  # Insert the data into the table
    connection.commit()  # Commit the changes to the database


if __name__ == "__main__":
    scraped = scrape(URL)  # Scrape the page source
    extracted = extract(scraped)  # Extract the temperature value
    print(extracted)  # Print the extracted value
    store(extracted)  # Store the value in the database