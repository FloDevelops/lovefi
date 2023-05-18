import json

with open('logs/transactions.json', 'r') as f:
    transactions = json.loads(f.read())['transactions']

for transaction in transactions:
    if transaction['account_id'] == '1E5xjd0zVgFKw5EqaaKesbE8rbXOdNSmDDz30':
        print(transaction['date'], transaction['amount'], transaction['iso_currency_code'], transaction['name'])