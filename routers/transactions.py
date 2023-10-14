import json
import pandas as pd
from fastapi import APIRouter
from typing import List
from models.transacations import Transaction
from models.summary import Summary
from utils.processing import (
    validate_and_fix_date,
    validate_and_fix_amount,
    clean_amount,
    clean_category
)
from utils.analyzer import calculate_summary
from utils.helper import get_collection
from schema.schemas import list_serial
from pymongo import UpdateOne

router = APIRouter(prefix="/transactions", tags=["Transactions"])
@router.post("/process")
def process_and_store_data(txs: List[Transaction]) -> bool:

    # Denormalize the data
    df = pd.json_normalize(
        [tx.to_dict() for tx in txs]
    )

    # Fix the Date values
    df["date"] = df["date"].apply(lambda x: validate_and_fix_date(x)[1])
    df["date"] = pd.to_datetime(df["date"], format="%Y-%m-%d")

    # Fix the Amount for non-numeric values
    df["amount"] = df["amount"].apply(lambda x: validate_and_fix_amount(x)[1])
    clean_amount(df)

    # Fill the missing values for the category
    mode_category = df[df["amount"] < 0]["category"].mode()
    mode_category = mode_category[0] if df.shape[0] > 1 else mode_category
    df["category"] = df[["amount", "category"]].apply(lambda x: clean_category(x, mode_category), axis=1)

    # Denormalize the location data
    df["location"] = {"city": df["location.city"], "region": df["location.region"]}
    del df["location.city"]
    del df["location.region"]

    # Save the Processed Data to the Database
    collection_name = get_collection()
    
    # create a list of update operations
    update_ops = []
    for obj in df.to_dict(orient="records"):
        update_ops.append(
            UpdateOne(
                {"transaction_id": obj["transaction_id"]},
                {"$set": obj},
                upsert=True
            )
        )

    # perform the bulk write operation
    collection_name.bulk_write(update_ops)

    # Return True if the data is processed and stored successfully
    return True

@router.post("/analyze")
def analyze_data(txs: List[Transaction]) -> dict:
    process_and_store_data(txs)

    # Collect all the transactions from the database
    collection_name = get_collection()
    transactions = list_serial(collection_name.find())

    df = pd.json_normalize(transactions)

    if df.shape[0] < 25:
        return {"error": "Not enough data to analyze"}
   
    #  Calculate the Summary here
    summary = calculate_summary(df)

    # Store Summary in the collection
    collection_name = get_collection(collection_name="summaries")
    collection_name.insert_one(summary)

    return Summary(**summary).to_dict()