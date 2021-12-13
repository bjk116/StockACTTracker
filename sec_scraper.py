import requests
import datetime

# zach will need to install this
# pip install beautifulsoup4
# if that doesn't work
# pip3 install beautifulsoup4
from bs4 import BeautifulSoup

# pip3 install requests-html
# or
# pip install 
# Required as sec website is created in js and needs to be rendered
from requests_html import HTMLSession

# comment out for now so this is runnable with minimimal install
#import db
#import queries


SEC_SENATE_STOCK_DISCLOSURE_URL = "https://sec.report/Senate-Stock-Disclosures"
# Possible transaction resource - DATA_SOURCE = "https://senate-stock-watcher-data.s3-us-west-2.amazonaws.com/aggregate/all_transactions_for_senators.json"

def getHTML():
    session = HTMLSession()
    r = session.get(SEC_SENATE_STOCK_DISCLOSURE_URL)
    r.html.render(sleep=1, keep_page=True, scrolldown=1)
    soup = BeautifulSoup(r.text, 'html.parser')
    return soup

def getDataTable(soup):
    return soup.find(class_='table')

def populateTransactions():
    soup = getHTML()
    table = getDataTable(soup)
    # Construct columns
    header_columns = []
    for header in table.find_all('th'):
        if len(header.find_all('a')) > 0:
            for link in header.find_all('a'):
                header_columns.append(link.text)
                print(f"apeending link text {link.text}")
        else:
            print(f"appending header text {header.text}")
            header_columns.append(header.text)
    print(header_columns)
    for row in table.tbody.find_all('tr'):
        columns = row.find_all('td')
        if len(columns) > 0:
            pass
    return table, header_columns