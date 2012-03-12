from settings import DB
from django.db import models

class Transaction(object):

    def __init__(self, owner, budget):
        self.transactions = DB.transactions
        self.transaction = {
            'owner' : owner,
            'budget' : budget,
            'sum' : 0,
            'description' : ''
        }
    
    def __init__(self, query):
        self.transactions = DB.transactions
        self.transaction = self.transactions.find_one(query)

    def get(self, query):
        return self.transactions.find(query)

    def get_one(self, query):
        return self.transactions.find_one(query)
        
    def save(self):
        self.transactions.save(self.transaction)