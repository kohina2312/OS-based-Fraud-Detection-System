import csv
from multiprocessing import Process
from threading import Thread
from fraud_detector import detect_fraud
from ipc_handler import send_to_log


def load_transactions(filename):
    transactions = []
    with open(filename, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            transaction = {
                "TransactionID": int(row["TransactionID"]),
                "Timestamp": row["Timestamp"],
                "Amount": float(row["Amount"]),
                "Location": row["Location"],
                "CardHolderID": int(row["CardHolderID"]),
                "MerchantID": int(row["MerchantID"]),
                "TransactionType": row["TransactionType"],
                "IsFraud": int(row["IsFraud"])
            }
            transactions.append(transaction)
    return transactions


def handle_transaction(transaction):
    result_container = {}

    def detect():
        result_container['data'] = detect_fraud(transaction)

    def log():
        detect_thread.join()
        send_to_log(result_container['data'])

    detect_thread = Thread(target=detect)
    log_thread = Thread(target=log)

    detect_thread.start()
    log_thread.start()

    detect_thread.join()
    log_thread.join()

def handle_transactions(transactions):
    processes = []

    for txn in transactions:
        p = Process(target=handle_transaction, args=(txn,))
        p.start()
        processes.append(p)

    for p in processes:
        p.join()


if __name__ == "__main__":
    filename = "data/transactions.csv"
    transactions = load_transactions(filename)
    handle_transactions(transactions)
