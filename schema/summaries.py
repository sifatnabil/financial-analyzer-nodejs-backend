def individual_serial(summary) -> dict:
    return {
        "id": str(summary["_id"]),
        "status": summary["status"],
        "totalSpending": summary["totalSpending"],
        "totalEarning": summary["totalEarning"],
        "totalSpendingPercentage": summary["totalSpendingPercentage"],
        "cautionDate": summary["cautionDate"],
        "metric": summary["metric"],
        "maxTransaction": summary["maxTransaction"],
        "modeMerchant": summary["modeMerchant"]
    }

def list_serial(summaries) -> list:
    return [individual_serial(summary) for summary in summaries]