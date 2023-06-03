import json
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate('secrets/sa.json')

app = firebase_admin.initialize_app(cred)
db = firestore.client()

with open('logs/transactions.json', 'r') as f:
    transactions = json.loads(f.read())['transactions']

for transaction in transactions:
    transaction_id = transaction['transaction_id']
    db.collection('transactions').document(transaction_id).set(transaction)
    if transaction['account_id'] == '1E5xjd0zVgFKw5EqaaKesbE8rbXOdNSmDDz30':
        print(transaction['date'], transaction['amount'], transaction['iso_currency_code'], transaction['name'])