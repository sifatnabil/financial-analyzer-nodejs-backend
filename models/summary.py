from typing import List
from pydantic import BaseModel
from datetime import datetime

class Summary(BaseModel):
    status: str
    totalSpending: float
    totalEarning: float
    total_spending_percentage: float
    cautionDate: datetime
    metric: float
    maxTransaction: float
    modeMerchant: str

    def to_dict(self):
        return {
            "status": self.status,
            "totalSpending": self.totalSpending,
            "totalEarning": self.totalEarning,
            "total_spending_percentage": self.total_spending_percentage,
            "cautionDate": self.cautionDate,
            "metric": self.metric,
            "maxTransaction": self.maxTransaction,
            "modeMerchant": self.modeMerchant
        }