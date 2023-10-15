from typing import List
from pydantic import BaseModel

class Difference(BaseModel):
    status: str | None = None
    totalSpending: str | None = None
    totalEarning: str | None = None
    totalSpendingPercentage: str | None = None
    cautionDate: str | None = None
    maxTransaction: str | None = None
    modeMerchant: str | None = None

    def to_dict(self):
        return {
            "status": self.status,
            "totalSpending": self.totalSpending,
            "totalEarning": self.totalEarning,
            "totalSpendingPercentage": self.totalSpendingPercentage,
            "cautionDate": self.cautionDate,
            "maxTransaction": self.maxTransaction,
            "modeMerchant": self.modeMerchant
        }