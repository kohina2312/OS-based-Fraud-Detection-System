import time
from datetime import datetime

user_last_activity = {}

def detect_fraud(transaction):
    fraud = False
    reasons = []

    amount = transaction["Amount"]
    user_id = transaction["CardHolderID"]
    location = transaction["Location"]
    timestamp = transaction["Timestamp"]
    txn_type = transaction["TransactionType"]

    # Rule 1: High amount (> ₹2000)
    if amount > 2000:
        fraud = True
        reasons.append("High transaction amount")

    # Rule 2: Rapid transactions (within 5 minutes)
    if user_id in user_last_activity:
        last_time = user_last_activity[user_id]["timestamp"]
        time_diff = get_time_diff_in_seconds(last_time, timestamp)
        if time_diff < 300:
            fraud = True
            reasons.append("Rapid multiple transactions")

    # Rule 3: New transaction location
    if user_id in user_last_activity:
        last_location = user_last_activity[user_id]["location"]
        if location != last_location:
            fraud = True
            reasons.append("New transaction location")

    if txn_type == "online" and user_id in user_last_activity:
        last_location = user_last_activity[user_id]["location"]
        if location != last_location:
            fraud = True
            reasons.append("Online transaction from new location")

    hour = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S").hour
    if 0 <= hour < 6 and amount > 1500:
        fraud = True
        reasons.append("Nighttime high amount transaction")

    # Update last activity
    user_last_activity[user_id] = {
        "timestamp": timestamp,
        "location": location
    }

    return {
        "TransactionID": transaction["TransactionID"],
        "IsFraud": fraud,
        "Reasons": reasons,
        "OriginalTransaction": transaction
    }

def get_time_diff_in_seconds(t1, t2):
    fmt = "%Y-%m-%d %H:%M:%S"
    time1 = time.strptime(t1, fmt)
    time2 = time.strptime(t2, fmt)
    return abs(time.mktime(time2) - time.mktime(time1))
