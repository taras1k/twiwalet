# -*- coding: utf-8 -*-
from settings import DB
from django.db import models

class TransactionModel(object):

    def __init__(self, owner=None, budget=None, category=None, money=None, description=None):
        self.transactions = DB.transactions
        self.transaction = {
            'owner' : owner,
            'budget' : budget,
            'category' : category,
            'money' : money,
            'description' : description
        }
    
    def get(self, query):
        return self.transactions.find(query)

    def get_one(self, query):
        return self.transactions.find_one(query)
        
    def save(self):
        self.transactions.save(self.transaction)