import logging
import datetime

from firebase_admin import credentials, initialize_app, firestore

# Initialize Firebase
cred = credentials.Certificate('secrets/sa.json')
app = initialize_app(cred)
db = firestore.client()


# USER
def get_user(user_id):
    logging.info(f'Getting user')
    user = db.collection('users').document(user_id).get().to_dict()
    response = {
        'operation': 'get_user',
        'user': user,
        'datetime': datetime.datetime.now()
    }
    return response


def update_cursor(cursor, item_id):
    logging.info(f'Updating cursor to {cursor}')
    db.collection('users').document('flo').update({
        f'items.{item_id}.last_sync': {
            'datetime': datetime.datetime.now(),
            'cursor': cursor
        }
    })
    logging.info(f'Updated cursor')
    response = {
        'operation': 'update_cursor',
        'cursor': cursor,
        'datetime': datetime.datetime.now()
    }
    return response



# TRANSACTION
def add_transactions(transactions):
    logging.info(f'Found {len(transactions)} new transactions')
    for transaction in transactions:
        transaction_id = transaction['transaction_id']
        transaction['_status'] = {
            'added': datetime.datetime.now()
        }
        db.collection('transactions').document(transaction_id).set(transaction)
    response = {
        'operation': 'add',
        'transactions': len(transactions),
        'datetime': datetime.datetime.now()
    }
    logging.info(f'Added {len(transactions)} new transactions')
    return response

def modify_transactions(transactions):
    logging.info(f'Found {len(transactions)} modified transactions')
    for transaction in transactions:
        transaction_id = transaction['transaction_id']
        transaction['_status'] = {
            'modified': datetime.datetime.now()
        }
        db.collection('transactions').document(transaction_id).update(transaction)
    response = {
        'operation': 'modify',
        'transactions': len(transactions),
        'datetime': datetime.datetime.now()
    }
    logging.info(f'Modified transactions')
    return response

def remove_transactions(transactions):
    logging.info(f'Found {len(transactions)} removed transactions')
    for transaction in transactions:
        transaction_id = transaction['transaction_id']
        db.collection('transactions').document(transaction_id).update({
            '_status': {
                'removed': datetime.datetime.now()
            },
            'removed': True
        })
    response = {
        'operation': 'remove',
        'transactions': len(transactions),
        'datetime': datetime.datetime.now()
    }
    logging.info(f'Removed transactions')
    return response

