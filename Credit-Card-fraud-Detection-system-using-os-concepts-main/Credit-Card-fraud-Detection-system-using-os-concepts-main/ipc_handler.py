import csv
import os

def send_to_log(result):
    txn_id = result["TransactionID"]
    status = "FRAUD" if result["IsFraud"] else "SAFE"
    reasons = ", ".join(result["Reasons"]) if result["Reasons"] else "None"
    print(f"\n[LOG] Transaction {txn_id} => {status} | Reasons: {reasons}")

    if result["IsFraud"]:
        confirm = input(f"[ALERT] Transaction {txn_id} is flagged as FRAUD. Do you want to allow it? (yes/no): ")
        if confirm.strip().lower() == "yes":
            print(f"[ACTION] User ALLOWED transaction {txn_id}. Proceeding...")
            send_otp(txn_id)
        else:
            print(f"[ACTION] Transaction {txn_id} BLOCKED by user.\n")
    else:
        send_otp(txn_id)
        log_safe_transaction(result["OriginalTransaction"])  # ✅ Save safe ones

def send_otp(txn_id):
    print(f"[OTP] Sending OTP for transaction {txn_id}... [OTP SENT]")

def log_safe_transaction(transaction):
    filename = "safe_transactions.csv"
    file_exists = os.path.exists(filename)

    with open(filename, mode='a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=[
            "TransactionID", "Timestamp", "Amount", "Location",
            "CardHolderID", "MerchantID", "TransactionType", "IsFraud"
        ])
        if not file_exists:
            writer.writeheader()
        writer.writerow(transaction)
