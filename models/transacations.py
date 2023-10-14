from typing import List
from pydantic import BaseModel

class Transaction(BaseModel):
    transaction_id: str
    date: str
    amount: str | float
    merchant: str
    category: List[str] | None = None
    location: dict
    payment_method: str

    def to_dict(self):
        return {
            "transaction_id": self.transaction_id,
            "date": self.date,
            "amount": self.amount,
            "merchant": self.merchant,
            "category": self.category,
            "location": self.location,
            "payment_method": self.payment_method
        }