import json
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate('secrets/sa.json')

app = firebase_admin.initialize_app(cred)
db = firestore.client()

with open('logs/transactions.json', 'r') as f:
    transactions = json.loads(f.read())
    added = transactions['added']
    modified = transactions['modified']
    removed = transactions['removed']
    datetime = transactions['datetime']
    cursor = transactions['cursor']

for transaction in added:
    transaction_id = transaction['transaction_id']
    db.collection('transactions').document(transaction_id).set(transaction)

for transaction in modified:
    transaction_id = transaction['transaction_id']
    db.collection('transactions').document(transaction_id).update(transaction)

for transaction_id in removed:
    db.collection('transactions').document(transaction_id).update({
        'removed': datetime
    })

db.collection('users').document('flo').update({
    'items': [
        {
            'id': 'j5qaENDdJMIpdP3XLLp1fg4JPyQALMuRnRAD6',
            'institution': 'Desjardins',
            'last_sync': {
                'datetime': datetime,
                'cursor': cursor
            }
        }
    ]
})