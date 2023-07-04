from flask import Flask
from datetime import datetime
import logging
import Plaid
import Firebase

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!<br><a href="/sync">Sync</a>'

@app.route('/sync')
def sync():
    user_data = Firebase.get_user('flo')['user']
    items = user_data['items']
    for item_id, item in items.items():
        transactions = Plaid.sync_transactions(item['access_token'], item['last_sync']['cursor'])

        Firebase.add_transactions(transactions['transactions']['added'])
        Firebase.modify_transactions(transactions['transactions']['modified'])
        Firebase.remove_transactions(transactions['transactions']['removed'])
        Firebase.update_cursor(transactions['transactions']['cursor'], item_id)

    response = {
        'operation': 'sync',
        'datetime': datetime.now()
    }
    return response

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=8080)