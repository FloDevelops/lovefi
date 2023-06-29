import json

earliest = None
biggest = None

with open('logs/transactions.json', 'r') as f:
    transactions = json.loads(f.read())['added']
    print(f'Found {len(transactions)} transactions')

for transaction in transactions:
    transaction_date = transaction['date']
    transaction_amount = transaction['amount']
    if earliest is None or transaction_date < earliest:
        earliest = transaction_date

    if biggest is None or transaction_amount > biggest:
        biggest = transaction_amount

print(f'Earliest transaction: {earliest}')
print(f'Biggest transaction: $ {biggest:,.2f}')