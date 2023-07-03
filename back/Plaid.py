import logging
import json
from os import getenv
import datetime

from dotenv import load_dotenv

from plaid.configuration import Configuration, Environment
from plaid.api_client import ApiClient
from plaid.api.plaid_api import PlaidApi
from plaid.model.transactions_sync_request import TransactionsSyncRequest
from plaid.model.transactions_sync_request_options import TransactionsSyncRequestOptions

load_dotenv()

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


def sync_transactions(access_token, cursor=None):
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
            access_token=access_token,
            cursor= cursor,
            count=500,
            options=options,
            )
        else:
            request = TransactionsSyncRequest(
            access_token=access_token,
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

    for array in [added, modified]:
        for transaction in array:
            transaction['date'] = datetime.datetime.combine(transaction['date'], datetime.datetime.min.time()) if transaction['date'] else None
            transaction['authorized_date'] = datetime.datetime.combine(transaction['authorized_date'], datetime.datetime.min.time()) if transaction['authorized_date'] else None

    # Print out the transactions
    results = dict(
        cursor = cursor,
        added = added,
        modified = modified,
        removed = removed,
        has_more = has_more,
        datetime = datetime.datetime.now()
    )
    
    # For logging only
    with open('logs/transactions.json', 'w') as f:
        f.write(json.dumps(
        results, 
        indent=2, 
        sort_keys=True, 
        default=str
        ))

    response = {
        'operation': 'sync_transactions',
        'transactions': results,
        'datetime': datetime.datetime.now()
    }
    return response
