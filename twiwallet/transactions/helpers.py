import jellyfish
from transactions.models import TransactionModel

JARO_SIMULARITY = 0.9

class Transaction(object):

    def __init__(self):
        self.budget_id = 0
        self.budget = ''
        self.category_id = 0
        self.category = ''
        self.money = 0
        self.description = ''
        self.owner = None

    def save_transaction(self):
        try:
            self.money = float(self.money)
        except ValueError:
            self.money = 0

        try:
            self.budget_id = int(self.budget_id)
        except ValueError:
            self.budget_id = 0

        try:
            self.category_id = int(self.category_id)
        except ValueError:
            self.category_id = 0
            
        t = TransactionModel(self.owner,
                        self.budget_id,
                        self.category_id,
                        self.money,
                        self.description)    
        t.save()

    def get_budget_sum(self, budget_id):
        t = TransactionModel()
        query =  {'budget': budget_id}
        budget_sum = 0
        for elemet in t.get(query):
            budget_sum += elemet['money']
        return budget_sum 



def get_similar(queryset, criteria):
    if not queryset.count():
        return 0
    result = {element.id:jellyfish.jaro_distance(element.name.encode('utf8'), 
                    criteria.encode('utf8')) for element in queryset}
    max_simular = max(result, key=result.get)
    if result[max_simular] > JARO_SIMULARITY:
        return max_simular
    else:
        return 0
