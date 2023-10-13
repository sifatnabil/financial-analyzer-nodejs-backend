import pandas as pd
import numpy as np
from datetime import datetime

def validate_and_fix_date(input_date):
    """Validates the dates and fixes them if they are in the future
    
    Args:
        input_date (str): Date string in the format YYYY-MM-DD

    Returns:
        bool: True if the date is valid, False otherwise
        str: The date string in the format YYYY-MM-DD
    """

    try:
        # Attempt to parse the input date string
        date_obj = datetime.strptime(input_date, "%Y-%m-%d")

        # Check if the year is in the future
        current_year = datetime.now().year
        if date_obj.year > current_year:
            date_obj = date_obj.replace(year=current_year)

        return True, date_obj.strftime("%Y-%m-%d")
    except ValueError:
        return False, None  # Date couldn't be fixed
    
def validate_and_fix_amount(input_amount):
    """Checks for invalid vaulues in the amount column and fixes them
    
    Args:
        input_amount (str): Amount string
    
    Returns:
        bool: True if the amount is valid, False otherwise
        float: The amount as a float
    """

    try:
        float(input_amount)
        return True, float(input_amount)
    except ValueError:
        return False, np.nan  # Amount couldn't be fixed
    
def clean_category(val, mode_category):
    """Fills the missing values in the category column based on the category
    
    Args:
        val (tuple): A tuple containing the amount and category
        mode_category (str): The mode category

    Returns:
        str: The category
    """

    amount, category = val[0], val[1]
    if category is not None:
        return category[0]
    else:
        return "Income" if amount > 0 else mode_category
    
def clean_amount(df):
    """Fills missing values for Amount column based on transaction category
    
    Args:
        df (DataFrame): The DataFrame containing the transactions
    
    Returns:
        None
    """

    mode_income = df["amount"][df["amount"] > 0].mean()
    mode_expense = df["amount"][df["amount"] < 0].mean()

    null_income_idx = df[(df["amount"].isna()) & (df["category"] == "Income")].index
    null_expense_idx = df[(df["amount"].isna()) & (df["category"] != "Income")].index
    
    df.loc[null_income_idx, "amount"] = round(mode_income, 2)
    df.loc[null_expense_idx, "amount"] = round(mode_expense, 2)