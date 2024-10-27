import requests
import selectorlib

from datetime import datetime


URL = "http://programmer100.pythonanywhere.com/"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

def scrape(url):
    """Scrape the page source from the URL"""  # Docstring explaining the function's purpose
    response = requests.get(url, headers=HEADERS)  # Fetch the webpage with specified headers
    source = response.text  # Extract the HTML content
    return source  # Return the HTML content


def extract(source):
    extractor = selectorlib.Extractor.from_yaml_file("extract.yaml")  # Load extraction rules from YAML
    value = extractor.extract(source)["tours"]  # Extract data based on the rules
    return value  # Return the extracted data


def store(extracted):
    now = datetime.now().strftime("%y-%m-%d-%H-%M-%S")  # Get current timestamp
    with open("data.txt", "a") as file:  # Open file in append mode
        line = f"{now},{extracted}\n"  # Format the data to be written
        file.write(line)  # Write the formatted data to the file


if __name__ == "__main__":
    scraped = scrape(URL)  # Scrape the webpage
    extracted = extract(scraped)  # Extract data from the scraped content
    print(extracted)  # Print the extracted data
    store(extracted)  # Store the extracted data in a file