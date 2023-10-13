import pandas as pd
from fastapi import APIRouter
from typing import List
from models.transacations import Transaction
from utils.processing import (
    validate_and_fix_date,
    validate_and_fix_amount,
    clean_amount,
    clean_category
)
from utils.analyzer import calculate_summary

router = APIRouter(prefix="/transactions", tags=["Transactions"])

@router.post("/process")
def process_and_store_data(txs: List[Transaction]):

    df = pd.json_normalize(
        [tx.to_dict() for tx in txs]
    )

    df["date"] = df["date"].apply(lambda x: validate_and_fix_date(x)[1])
    df["date"] = pd.to_datetime(df["date"], format="%Y-%m-%d")

    df["amount"] = df["amount"].apply(lambda x: validate_and_fix_amount(x)[1])

    clean_amount(df)

    mode_category = df[df["amount"] < 0]["category"].mode()
    mode_category = mode_category[0] if df.shape[0] > 1 else mode_category
    df["category"] = df[["amount", "category"]].apply(lambda x: clean_category(x, mode_category), axis=1)

    # TODO: Insert data into the database

    return df.to_dict(orient="records")

@router.post("/analyze")
def analyze_data(txs: Transaction) -> dict:
    df = process_and_store_data(txs.transactions)

    # TODO: Fetch data from the database
   
    # * Calculate the Summary here
    summary = calculate_summary(df)

    return summary