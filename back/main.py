import logging
import json
from os import getenv
import datetime

from dotenv import load_dotenv

from firebase_admin import credentials, initialize_app, firestore

from plaid.configuration import Configuration, Environment
from plaid.api_client import ApiClient
from plaid.api.plaid_api import PlaidApi
from plaid.model.transactions_sync_request import TransactionsSyncRequest
from plaid.model.transactions_sync_request_options import TransactionsSyncRequestOptions

load_dotenv()

# Initialize Firebase
cred = credentials.Certificate('secrets/sa.json')
app = initialize_app(cred)
db = firestore.client()

# Initialize Plaid
PLAID_ENV = getenv('PLAID_ENV')
if PLAID_ENV == 'sandbox':
    host = Environment.Sandbox
    PLAID_SECRET=getenv('PLAID_SECRET_SANDBOX')

if PLAID_ENV == 'development':
    host = Environment.Development
    PLAID_SECRET=getenv('PLAID_SECRET_DEVELOPMENT')

if PLAID_ENV == 'production':
    host = Environment.Production
    PLAID_SECRET=getenv('PLAID_SECRET_PRODUCTION')

PLAID_CLIENT_ID=getenv('PLAID_CLIENT_ID')
PLAID_PRODUCTS = getenv('PLAID_PRODUCTS')
PLAID_COUNTRY_CODES = getenv('PLAID_COUNTRY_CODES')
PLAID_REDIRECT_URI=None

configuration = Configuration(
    host=host,
    api_key={
        'clientId': PLAID_CLIENT_ID,
        'secret': PLAID_SECRET,
    }
)

api_client = ApiClient(configuration)
client = PlaidApi(api_client)

# We store the access_token in memory - in production, store it in a secure
# persistent data store.
ACCESS_TOKEN = getenv('ACCESS_TOKEN')
ITEM_ID = getenv('ITEM_ID')

# Function to get the current cursor
def get_cursor():
  user = db.collection('users').document('flo').get().to_dict()

  try:
    cursor = user['items'][0]['last_sync']['cursor']
  except:
    cursor = None

  return cursor

def get_transactions(cursor=None):
  added = []
  modified = []
  removed = [] # Removed transaction ids
  has_more = True
  options = TransactionsSyncRequestOptions(
      include_personal_finance_category = True
  )
  # Iterate through each page of new transaction updates for item
  while has_more:
      if cursor:
          request = TransactionsSyncRequest(
          access_token=ACCESS_TOKEN,
          cursor= cursor,
          count=500,
          options=options,
          )
      else:
          request = TransactionsSyncRequest(
          access_token=ACCESS_TOKEN,
          count=500,
          options=options,
          )

      response = client.transactions_sync(request).to_dict()
      # Add this page of results
      added.extend(response['added'])
      modified.extend(response['modified'])
      removed.extend(response['removed'])
      has_more = response['has_more']
      # Update cursor to the next cursor
      cursor = response['next_cursor']

  # Print out the transactions
  results = dict(
      cursor = cursor,
      added = added,
      modified = modified,
      removed = removed,
      has_more = has_more,
      datetime = datetime.datetime.now()
  )

  logging.info(f'Found {len(added)} new transactions')
  for transaction in added:
      transaction_id = transaction['transaction_id']
      db.collection('transactions').document(transaction_id).set(transaction)
  logging.info(f'Added new transactions')

  logging.info(f'Found {len(modified)} modified transactions')
  for transaction in modified:
      transaction_id = transaction['transaction_id']
      db.collection('transactions').document(transaction_id).update(transaction)
  logging.info(f'Modified transactions')

  logging.info(f'Found {len(removed)} removed transactions')
  for transaction_id in removed:
      db.collection('transactions').document(transaction_id).update({
          'removed': results['datetime']
      })
  logging.info(f'Removed transactions')

  logging.info(f'Updating cursor to {cursor}')
  db.collection('users').document('flo').update({
      'items': [
          {
              'id': 'j5qaENDdJMIpdP3XLLp1fg4JPyQALMuRnRAD6',
              'institution': 'Desjardins',
              'last_sync': {
                  'datetime': results['datetime'],
                  'cursor': cursor
              }
          }
      ]
  })
  logging.info(f'Updated cursor')


  # For logging only
  with open('logs/transactions.json', 'w') as f:
    f.write(json.dumps(
      results, 
      indent=2, 
      sort_keys=True, 
      default=str
    ))

if __name__ == '__main__':
  cursor = get_cursor()
  get_transactions(cursor=cursor)