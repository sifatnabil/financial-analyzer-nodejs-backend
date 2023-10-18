import pandas as pd
import numpy as np
from pandas import DataFrame


def calculate_summary(df: DataFrame) -> dict:
    """ Calculate the summary of the transaction data
        Args:
            df: DataFrame containing the transaction data
        
        Returns:
            dict: A dictionary containing the summary of the transaction data
    """
    
    # Find The Current total spending and earning
    total_spending = round(df[df["amount"] < 0]["amount"].sum(), 2)
    total_earning = round(df[df["amount"] > 0]["amount"].sum(), 2)

    # Find the Percentage of spending and earning
    total_spending_percentage = round(
        abs(total_spending) / total_earning * 100
    , 2)

    # * Sort the database by transaction dates
    df = df.sort_values(by="date")

    df['Income'] = 0
    df['Spending'] = 0

    # Set the values for income and spending based on the 'category'
    df.loc[df['category'] == 'Income', 'Income'] = \
        df.loc[df['category'] == 'Income', 'amount']
    df.loc[df['category'] != 'Income', 'Spending'] = \
        abs(df.loc[df['category'] != 'Income', 'amount'])

    # Add date information to the dataframe
    df = df.assign(
        day_of_month=df["date"].dt.day, 
        month=df["date"].dt.month, 
        year=df["date"].dt.year
    )

    # Create a daily summary of user transactions
    daily_summary = df.groupby(["date", "day_of_month", "month", "year"]).agg(
        total_income=("Income", "sum"),
        total_spending=("Spending", "sum"),
        transaction_count=('transaction_id', 'count'),
        unique_merchants=('merchant', 'nunique')
    ).sort_values(by="date").reset_index()

    # Create a monthly summary of user transactions
    monthly_summary = df.groupby(["month", "year"]).agg(
        date_min=("date", "min"),
        date_max=("date", "max"),
        total_income=("Income", "sum"),
        total_spending=("Spending", "sum"),
        transaction_count=('transaction_id', 'count'),
        unique_merchants=('merchant', 'nunique')
    ).sort_values(by=["year", "month"]).reset_index()

    # Calculate cumulative net worth as the months go by
    monthly_summary["cumulative_net"] = \
        (monthly_summary['total_income'] - monthly_summary['total_spending']).cumsum()

    # Calculate average monthly income as the months go by
    monthly_summary["cumulative_average"] = \
        monthly_summary['total_spending'].cumsum() / monthly_summary["month"]
    
    # Calculate the net difference between the previous and current month
    last_month_net = monthly_summary["cumulative_net"].iloc[-2]
    current_month_net = monthly_summary["cumulative_net"].iloc[-1]
    net_difference = current_month_net - last_month_net
    net_difference_percentage = round(
        net_difference / current_month_net * 100, 2
    )

    # Calculate the average spending including the before and including the latest month
    prev_avg = monthly_summary["cumulative_average"].iloc[-2]
    cur_avg = monthly_summary["cumulative_average"].iloc[-1]

    # Check for anomaly between financial behavior and income
    # If the current spending is greater than the previous average
    if (cur_avg > prev_avg) \
    and (net_difference_percentage < 0) \
    and abs(net_difference_percentage) > 5:
        # Filter out the latest month data
        latest_month = daily_summary["month"].max()
        latest_year = daily_summary["year"].max()
        
        last_month_daily_summary = \
            daily_summary[(daily_summary["month"] == latest_month) & \
                          (daily_summary["year"] == latest_year)]
        
        last_month_daily_summary['cumulative_sum'] = \
            last_month_daily_summary['total_spending'].cumsum()
        
        
        # Select the indexes to find out the anmaly rows
        caution_idx = \
            last_month_daily_summary[
                (last_month_daily_summary['cumulative_sum'] > cur_avg) & \
                (last_month_daily_summary['total_income'] == 0)
            ].index
        
        # Find the Anomaly Date
        caution_date = last_month_daily_summary.loc[caution_idx, "date"].min()

        # Filter out the anomaly rows
        caution_df = last_month_daily_summary.loc[caution_idx].merge(df, on="date", how="left")
        
        
        caution_merchant = caution_df["merchant"].mode()[0]
        caution_amount = caution_df["total_spending"].max()

        last_month_cumulative_avg = last_month_daily_summary["cumulative_sum"].iloc[-1]
        caution_metric = \
            round((last_month_cumulative_avg - prev_avg) / max(prev_avg, 1)  * 100, 2)
        
        # TODO: Last Income Comparison
    
        return {
            "status": "anomaly",
            "totalSpending": total_spending,
            "totalEarning": total_earning,
            "totalSpendingPercentage": total_spending_percentage,
            "cautionDate": caution_date,
            "metric": caution_metric,
            "maxTransaction": caution_amount,
            "modeMerchant": caution_merchant,
        }
    
    return {
        "status": "normal",
        "totalSpending": total_spending,
        "totalEarning": total_earning,
        "totalSpendingPercentage": total_spending_percentage,
        "cautionDate": None,
        "metric": None,
        "maxTransaction": daily_summary["total_spending"].max(),
        "modeMerchant": df[df["amount"] < 0]["merchant"].mode()[0],
    }

def calculate_difference(prev_summaries, current_summary):
    """
        Calculate the difference between the previous and current summary

        Args:
            prev_summaries: A list of previous summaries
            current_summary: The current summary

        Returns:
            dict: A dictionary containing the difference between the previous and current summary    
    """

    # If there are no previous summary to compare with return the current summary
    if not prev_summaries:
        return {
            "status": "",
            "totalSpending": "",
            "totalEarning": "",
            "totalSpendingPercentage": "",
            "cautionDate": "",
            "metric": "",
            "maxTransaction": "",
            "modeMerchant": ""
        }
    
    prev_summaries_df = pd.json_normalize(prev_summaries)
    current_summary_df = pd.json_normalize(current_summary)

    # Calculate separate field values for comparison
    # Status and caution date check with last summary
    last_status = prev_summaries_df["status"].iloc[-1]
    current_status = current_summary_df["status"].iloc[-1]

    if last_status == "nomral" and current_status == "normal":
        status = "financial status is good"
        caution_date = "Nothing for now"
    elif last_status == "normal" and current_status == "anomaly":
        status = "Should be careful with spending"
        caution_date = f"Anomaly detected on {current_summary_df['cautionDate'].iloc[-1]}"
    elif last_status == "anomaly" and current_status == "normal":
        status = "current status is improving, should continue"
        caution_date = f"Last Anomaly detected on {prev_summaries_df['cautionDate'].iloc[-1]}"
    elif last_status == "anomaly" and current_status == "anomaly":
        status = "should be really careful with spending"
        caution_date = f"Last Anomaly detected on {prev_summaries_df['cautionDate'].iloc[-1]} and still continuing"

    # Total Spending
    last_total_spending = prev_summaries_df["totalSpending"].iloc[-1]
    current_total_spending = current_summary_df["totalSpending"].iloc[-1]
    print(current_summary_df.head())
    if abs(last_total_spending) < abs(current_total_spending):
        total_spending = f"Spendings increased by {round(abs(current_total_spending) - abs(last_total_spending), 2)}"
    else: 
        total_spending = "Spending amount is the same"

    # Total Earning
    last_total_earning = prev_summaries_df["totalEarning"].iloc[-1]
    current_total_earning = current_summary_df["totalEarning"].iloc[-1]
    if last_total_earning < current_total_earning:
        total_earning = f"Earning increased by {round(abs(current_total_earning) - abs(last_total_earning), 2)}"
    else:
        total_earning = "Earning amount is the same"

    # Total Spending Percentage
    last_total_spending = prev_summaries_df["totalSpendingPercentage"].iloc[-1]
    current_total_spending = current_summary_df["totalSpendingPercentage"].iloc[-1]
    if last_total_spending < current_total_spending:
        total_spending_percentage = f"Spending Percentage increased by {round(abs(current_total_spending) - abs(last_total_spending), 2)}"
    else:
        total_spending_percentage = "Spending Percentage is the same"

    # Max Transaction
    last_max_transaction = prev_summaries_df["maxTransaction"].iloc[-1]
    current_max_transaction = current_summary_df["maxTransaction"].iloc[-1]
    if last_max_transaction < current_max_transaction:
        max_transaction = f"Max Transaction increased by {abs(current_max_transaction) - abs(last_max_transaction)}"
    elif last_max_transaction == current_max_transaction:
        max_transaction = f"Max Transaction is the same"
    else: 
        max_transaction = f"Max Transaction decreased by {abs(current_max_transaction) - abs(last_max_transaction)}"
    
    # Mode Merchant
    last_mode_merchant = prev_summaries_df["modeMerchant"].iloc[-1]
    current_mode_merchant = current_summary_df["modeMerchant"].iloc[-1]
    if last_mode_merchant != current_mode_merchant:
        mode_merchant = f"You are spending more on {last_mode_merchant} which was previously {current_mode_merchant}"
    else:
        mode_merchant = f"You are still spending the most on {last_mode_merchant}"
        
    return {
        "status": status,
        "totalSpending": total_spending,
        "totalEarning": total_earning,
        "totalSpendingPercentage": total_spending_percentage,
        "cautionDate": caution_date,
        "maxTransaction": max_transaction,
        "modeMerchant": mode_merchant
    }