def individual_serial(transaction) -> dict:
    return {
        "id": str(transaction["_id"]),
        "transaction_id": transaction["transaction_id"],
        "date": transaction["date"],
        "amount": transaction["amount"],
        "merchant": transaction["merchant"],
        "category": transaction["category"],
        "location": transaction["location"],
        "payment_method": transaction["payment_method"]
    }

def list_serial(transactions) -> list:
    return [individual_serial(transaction) for transaction in transactions]