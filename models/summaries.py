from typing import List
from pydantic import BaseModel
from datetime import datetime

class Summary(BaseModel):
    status: str
    totalSpending: float
    totalEarning: float
    totalSpendingPercentage: float
    cautionDate: datetime | None = None
    metric: float | None = None
    maxTransaction: float | None = None
    modeMerchant: str | None = None

    def to_dict(self):
        return {
            "status": self.status,
            "totalSpending": self.totalSpending,
            "totalEarning": self.totalEarning,
            "totalSpendingPercentage": self.totalSpendingPercentage,
            "cautionDate": self.cautionDate,
            "metric": self.metric,
            "maxTransaction": self.maxTransaction,
            "modeMerchant": self.modeMerchant
        }