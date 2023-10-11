import pandas as pd
from fastapi import APIRouter
from models.request_models import Transactions
from utils.processing import (
    create_dataframe,
    validate_and_fix_date,
    validate_and_fix_amount,
    clean_amount,
    clean_category
)

router = APIRouter()

@router.post("/process")
def process_and_store_data(txs: Transactions):
    df = create_dataframe(txs.transactions)

    df["date"] = df["date"].apply(lambda x: validate_and_fix_date(x)[1])
    df["date"] = pd.to_datetime(df["date"], format="%Y-%m-%d")

    df["amount"] = df["amount"].apply(lambda x: validate_and_fix_amount(x)[1])

    mode_category = df[df["amount"] < 0]["category"].mode()[0]
    df["category"] = df[["amount", "category"]].apply(lambda x: clean_category(x, mode_category), axis=1)

    clean_amount(df)

    return df.to_dict(orient="records")

@router.post("/analyze")
def analyze_data(txs: Transactions):
    return process_and_store_data(txs)