from flask import Flask, render_template, request, redirect, url_for, flash
import csv
import os
import pyotp
from fraud_detector import detect_fraud

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a secure key

# Temporary storage for OTP secrets
otp_store = {}

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files["file"]
        if file:
            file.save("transactions.csv")
            return redirect(url_for("results"))
    return render_template("index.html")

@app.route("/results")
def results():
    transactions = []
    with open("transactions.csv", "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            txn = {
                "TransactionID": int(row["TransactionID"]),
                "Timestamp": row["Timestamp"],
                "Amount": float(row["Amount"]),
                "Location": row["Location"],
                "CardHolderID": int(row["CardHolderID"]),
                "MerchantID": int(row["MerchantID"]),
                "TransactionType": row["TransactionType"],
                "IsFraud": int(row["IsFraud"])
            }
            result = detect_fraud(txn)
            if result["IsFraud"]:
                transactions.append(result)
    return render_template("results.html", transactions=transactions)

@app.route("/otp/<int:txn_id>")
def otp(txn_id):
    secret = pyotp.random_base32()
    totp = pyotp.TOTP(secret)
    otp_code = totp.now()
    otp_store[txn_id] = secret
    print(f"[OTP] Transaction {txn_id}: {otp_code}")  # In production, send via SMS or email
    return render_template("otp.html", txn_id=txn_id)

@app.route("/verify_otp/<int:txn_id>", methods=["POST"])
def verify_otp(txn_id):
    user_otp = request.form.get("otp")
    secret = otp_store.get(txn_id)
    if not secret:
        flash("OTP session expired or invalid transaction ID.")
        return redirect(url_for("results"))
    totp = pyotp.TOTP(secret)
    if totp.verify(user_otp):
        flash(f"✅ Transaction {txn_id} approved.")
        # Implement approval logic here
    else:
        flash("❌ Invalid OTP. Transaction blocked.")
        # Implement blocking logic here
    otp_store.pop(txn_id, None)
    return redirect(url_for("results"))

@app.route("/block/<int:txn_id>")
def block(txn_id):
    flash(f"❌ Transaction {txn_id} blocked.")
    # Implement blocking logic here
    return redirect(url_for("results"))

@app.route("/safe")
def safe_transactions():
    safe_txns = []
    if os.path.exists("safe_transactions.csv"):
        with open("safe_transactions.csv") as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Convert to correct types
                safe_txns.append({
                    "TransactionID": int(row["TransactionID"]),
                    "Timestamp": row["Timestamp"],
                    "Amount": float(row["Amount"]),
                    "Location": row["Location"],
                    "CardHolderID": int(row["CardHolderID"]),
                    "MerchantID": int(row["MerchantID"]),
                    "TransactionType": row["TransactionType"]
                })
    return render_template("safe.html", transactions=safe_txns)


if __name__ == "__main__":
    app.run(debug=True)
