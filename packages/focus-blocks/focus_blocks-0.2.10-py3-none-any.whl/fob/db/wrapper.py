from tinydb import TinyDB, Query

class TinyDBWrapper:
    '''
    Absolutely minimalist wrapper around TinyDB
    Just to not repeat db_path all the time.
    '''
    def __init__(self, db_path):
        # Initialize the TinyDB instance with the provided path
        self.db = TinyDB(db_path)
        self.query = Query()

    def insert(self, data):
        # Insert a document (dictionary) into the database
        return self.db.insert(data)

    def upsert(self, fields, query):
        return self.db.upsert(fields, query)

    def all(self):
        # Get all documents stored in the database
        return self.db.all()

    def search(self, query):
        # Search for documents based on the provided query
        return self.db.search(query)

    def update(self, fields, query):
        # Update documents matching the query with new fields
        return self.db.update(fields, query)

    def remove(self, query):
        # Remove documents matching the query
        return self.db.remove(query)

    def truncate(self):
        # Remove all documents from the database
        return self.db.truncate()
