
import json
from os import getenv
import datetime

from dotenv import load_dotenv
# from flask import Flask, jsonify, render_template, request

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

import plaid
from plaid.api import plaid_api
from plaid.model.transactions_sync_request import TransactionsSyncRequest
from plaid.model.transactions_sync_request_options import TransactionsSyncRequestOptions
# from plaid.model.transactions_get_request import TransactionsGetRequest
# from plaid.model.transactions_get_request_options import TransactionsGetRequestOptions

load_dotenv()

# Initialize Firebase
cred = credentials.Certificate('secrets/sa.json')
app = firebase_admin.initialize_app(cred)
db = firestore.client()


PLAID_ENV = getenv('PLAID_ENV')
if PLAID_ENV == 'sandbox':
    host = plaid.Environment.Sandbox
    PLAID_SECRET=getenv('PLAID_SECRET_SANDBOX')

if PLAID_ENV == 'development':
    host = plaid.Environment.Development
    PLAID_SECRET=getenv('PLAID_SECRET_DEVELOPMENT')

if PLAID_ENV == 'production':
    host = plaid.Environment.Production
    PLAID_SECRET=getenv('PLAID_SECRET_PRODUCTION')

PLAID_CLIENT_ID=getenv('PLAID_CLIENT_ID')
PLAID_PRODUCTS = getenv('PLAID_PRODUCTS')
PLAID_COUNTRY_CODES = getenv('PLAID_COUNTRY_CODES')
PLAID_REDIRECT_URI=None

configuration = plaid.Configuration(
    host=host,
    api_key={
        'clientId': PLAID_CLIENT_ID,
        'secret': PLAID_SECRET,
    }
)

api_client = plaid.ApiClient(configuration)
client = plaid_api.PlaidApi(api_client)

# We store the access_token in memory - in production, store it in a secure
# persistent data store.
ACCESS_TOKEN = getenv('ACCESS_TOKEN')
ITEM_ID = getenv('ITEM_ID')

user = db.collection('users').document('flo').get().to_dict()
try:
    cursor = user['items'][0]['last_sync']['cursor']
except:
    cursor = None # Keep track of current cursor

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
with open('logs/transactions.json', 'w') as f:
    f.write(json.dumps(
        results, 
        indent=2, 
        sort_keys=True, 
        default=str
    ))

