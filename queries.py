"""
Separating Query layer from rest of application
"""
import db

def saveCongressmen(congressmen):
    """
    Saves congrsessmen into the congressman TABLE in db.
    Args:
        congressmen: list of dictionaries with keys as column names and values as the value
    Returns:
        None
    """
    for data in congressmen:
        name = data['name'].replace("'", "\\'").strip()
        query = f"INSERT INTO congressman (state, party, position, full_name) VALUES ('{data['State']}', '{data['party']}', '{data['position']}', '{name}')"
        db.runUpdateQuery(query)

def saveTransaction(transactions):
    """
    Saves a transaction from the sec scraper to db.
    Args:
        transaction: list of dictionarys with transaction data
    Returns:
        None
    """
    for transaction in transactions:
        pass