# data_generator.py

import csv
import random
from datetime import datetime, timedelta

def generate_transaction_data(num_records):
    transactions = []
    for i in range(1, num_records + 1):
        is_fraud = random.choices([0, 1], weights=[90, 10])[0]

        if is_fraud:
            amount = round(random.uniform(1000.0, 5000.0), 2)
            location = random.choice(['Russia', 'North Korea', 'Unknown'])
        else:
            amount = round(random.uniform(10.0, 999.99), 2)
            location = random.choice(['New York', 'London', 'Mumbai', 'Berlin', 'Sydney'])

        txn = [
            i,
            (datetime.now() - timedelta(minutes=random.randint(0, 10000))).strftime('%Y-%m-%d %H:%M:%S'),
            amount,
            location,
            random.randint(1000, 9999),  # CardHolderID
            random.randint(100, 999),   # MerchantID
            random.choice(['online', 'instore']),
            is_fraud
        ]
        transactions.append(txn)
    return transactions
def save_to_csv(filename, transactions):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([
            'TransactionID', 'Timestamp', 'Amount', 'Location',
            'CardHolderID', 'MerchantID', 'TransactionType', 'IsFraud'
        ])
        writer.writerows(transactions)
if __name__ == "__main__":
    data = generate_transaction_data(1000)
    save_to_csv("transactions.csv", data)
    print("transactions.csv generated successfully!")
