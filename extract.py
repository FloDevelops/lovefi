
import json
from os import getenv
import datetime

from dotenv import load_dotenv
# from flask import Flask, jsonify, render_template, request

import plaid
from plaid.api import plaid_api
from plaid.model.transactions_get_request import TransactionsGetRequest
from plaid.model.transactions_get_request_options import TransactionsGetRequestOptions

load_dotenv()
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

request = TransactionsGetRequest(
    access_token=ACCESS_TOKEN,
    start_date=datetime.date(2023, 1, 1),
    end_date=datetime.date.today(),
    options=TransactionsGetRequestOptions()
)
response = client.transactions_get(request)
# transactions = response['transactions']

# print(json.dumps(response.to_dict(), indent=2, sort_keys=True, default=str))

# Manipulate the count and offset parameters to paginate
# transactions and retrieve all available data
# while len(transactions) < response['total_transactions']:
#     request = TransactionsGetRequest(
#         access_token=ACCESS_TOKEN,
#         start_date=datetime.date(2023, 5, 1),
#         end_date=datetime.date(2023, 5, 17),
#         options=TransactionsGetRequestOptions(
#         offset=len(transactions)
#         )
# )
# response = client.transactions_get(request)
# transactions.extend(response['transactions'])

with open('logs/transactions.json', 'w') as f:
    f.write(json.dumps(response.to_dict(), indent=2, sort_keys=True, default=str))

