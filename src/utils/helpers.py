from tabulate import tabulate
from json import loads

def print_table(data,columns=None):
    if type(data) == str:
        data = loads(data)
    if 'data' in data:
        data = data['data'] 
    if columns:
        data = [{col: row.get(col, None) for col in columns} for row in data]
    print(tabulate(data, headers="keys"))

def check_next(data):
    if type(data) == str:
        data = loads(data)
    if 'links' in data:
        if 'next' in data['links']:
            return data['links']['next']
    return None 