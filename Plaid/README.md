# MY PERSONAL FINANCES

THIS IS A PERSONNAL PROJECT UNDER DEVELOPMENT...
## HOW TO

### FETCH LATEST TRANSACTIONS FOR ME

Run extract.py (uses the environment variables in .env to connect to plaid and fetch a specific connection / access token).

### RENEW ACCESS TOKEN

View Plaid documentation for more information (previous tokens savd under logs/token.json).


## DEFINITIONS

- link_token: to start a user bank identification, generate a token specific to the user_id from my server and send frontend.
- public_token: when a user finishes the bank authentification, he receives a public_token frontend.
- access_token: when passed backend, the public_token is exchanged for an access_token and an item_id.