import requests
from bs4 import BeautifulSoup
import datetime
import db
import queries

SENATOR_DATA_SOURCE = "https://en.wikipedia.org/wiki/List_of_current_United_States_senators"
REPRESENTATIVE_DATA_SOURCE = "https://en.wikipedia.org/wiki/List_of_current_members_of_the_United_States_House_of_Representatives"

# Follow this - https://medium.com/geekculture/web-scraping-tables-in-python-using-beautiful-soup-8bbc31c5803e

def cleanText(text):
    BAD_CHARACTERS = ['\n', '[2]', '[a]', '\xa0']
    for bad_character in BAD_CHARACTERS:
        text = text.replace(bad_character, '')
    return text

def getSenators():
    """
    Populate congressman table with list of current US Senators
    """
    s = requests.Session()
    r = s.get(f"{SENATOR_DATA_SOURCE}")
    soup = BeautifulSoup(r.text, 'html.parser')
    table = soup.find(id='senators')
    table_data = []
    count = 0
    # Weird one as only odd numbered rows seem to actually have the state so we want the even number ones to get it from the previous record
    state = None
    for row in table.tbody.find_all('tr'):
        columns = row.find_all('td')
        header_columns = row.find('th')
        if len(columns) > 0:
            count += 1
            if count % 2 == 0:
                # TODO - Make second two replaces a regex that replaces anything of the format [sometext]
                party = columns[2].text
            else:
                party = columns[3].text
                state = columns[0].text
            data = {
                "State":cleanText(state), 
                "position":"senator",
                "name":cleanText(row.find('th').text),
                "party":cleanText(party)
            }
            print(data)
            table_data.append(data)
    return table_data

def getRepresentatives():
    """
    Populate congrssman wth table of current US Representatives
    """
    s = requests.Session()
    r = s.get(f"{REPRESENTATIVE_DATA_SOURCE}")
    soup = BeautifulSoup(r.text, 'html.parser')
    table = soup.find(id='votingmembers')
    table_data = []
    count = 0
    for row in table.tbody.find_all('tr'):
        columns = row.find_all('td')
        if len(columns) > 0 and cleanText(columns[1].text) != 'VACANT':
            data = {
                "State":cleanText(columns[0].text),
                "position": "representative",
                "name":cleanText(columns[1].text),
                "party":cleanText(columns[3].text)
            }
            table_data.append(data)
            count += 1
    return table_data

def clearTables():
    clear_transaction_query = "DELETE FROM transactions"
    reset_transaction_id = "ALTER TABLE transactions AUTO_INCREMENT=1"
    clear_congressman_query = "DELETE FROM congressman"
    reset_congressman_id = "ALTER TABLE congressman AUTO_INCREMENT=1"
    queries = [clear_transaction_query, reset_transaction_id, clear_congressman_query, reset_congressman_id]
    for query in queries:
        db.runUpdateQuery(query)    

def fillDatabase():
    """
    Gets list of senators/congressman and fills in table.
    """
    clearTables()
    senators = getSenators()
    queries.saveCongressmen(senators)
    representatives = getRepresentatives()
    queries.saveCongressmen(representatives)
    return None

if __name__ == "__main__":
    fillDatabase()