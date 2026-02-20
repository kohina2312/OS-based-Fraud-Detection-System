# logger.py

import os
from datetime import datetime

def log_result(result):
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, "fraud_log.txt")

    with open(log_file, "a") as file:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        txn_id = result["TransactionID"]
        amount = result["OriginalTransaction"]["Amount"]
        status = "FRAUD" if result["IsFraud"] else "SAFE"
        reasons = ", ".join(result["Reasons"]) if result["Reasons"] else "None"

        line = f"[{timestamp}] TransactionID: {txn_id} | Amount: {amount} | Status: {status} | Reasons: {reasons}\n"
        file.write(line)
