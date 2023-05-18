
import json
from os import getenv
import time

from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, request

import plaid
from plaid.api import plaid_api
from plaid.model.products import Products
from plaid.model.country_code import CountryCode
from plaid.model.link_token_create_request import LinkTokenCreateRequest
from plaid.model.link_token_create_request_user import LinkTokenCreateRequestUser
from plaid.model.item_public_token_exchange_request import ItemPublicTokenExchangeRequest

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

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True


configuration = plaid.Configuration(
    host=host,
    api_key={
        'clientId': PLAID_CLIENT_ID,
        'secret': PLAID_SECRET,
    }
)

api_client = plaid.ApiClient(configuration)
client = plaid_api.PlaidApi(api_client)

products = []
for product in PLAID_PRODUCTS:
    products.append(Products(product))

# We store the access_token in memory - in production, store it in a secure
# persistent data store.
access_token = None
item_id = None


@app.get("/")
def hello():
    return  render_template('index.html')

@app.post('/api/create-link-token')
def create_link_token():
    try:
        request = LinkTokenCreateRequest(
            # products=products,
            products=[Products('transactions')],
            client_name="Plaid Quickstart",
            # country_codes=list(map(lambda x: CountryCode(x), PLAID_COUNTRY_CODES)),
            country_codes=[CountryCode('CA')],
            language='en',
            user=LinkTokenCreateRequestUser(
                client_user_id=str(time.time())
            )
        )
        if PLAID_REDIRECT_URI!=None:
            request['redirect_uri']=PLAID_REDIRECT_URI

        # create link token
        response = client.link_token_create(request)
        return jsonify(response.to_dict())
    except plaid.ApiException as e:
        return json.loads(e.body)
    

@app.post('/api/get-access-token')
def get_access_token():
    global access_token
    global item_id
    global transfer_id
    data = request.get_json()
    public_token = data['public_token']
    print('public_token:', public_token)
    try:
        exchange_request = ItemPublicTokenExchangeRequest(
            public_token=public_token
        )
        exchange_response = client.item_public_token_exchange(exchange_request)
        access_token = exchange_response['access_token']
        print('access_token:', access_token)
        item_id = exchange_response['item_id']
        print('item_id:', item_id)
        print('exchange_response:', exchange_response.to_dict())
        return jsonify(exchange_response.to_dict())
    except plaid.ApiException as e:
        return json.loads(e.body)
    
if __name__ == '__main__':
    app.run(port=8000)
