
import pandas as pd
from pathlib import Path

print("Starting SaaS Churn Analysis...")

# Locate the project and dataset
PROJECT_DIR = Path(__file__).resolve().parent
DATA_FILE = PROJECT_DIR / "data" / "Telco-Customer-Churn.csv"

print("Project folder:", PROJECT_DIR)
print("Looking for dataset:", DATA_FILE)

# Check that the dataset exists
if not DATA_FILE.exists():
    print("\nERROR: Dataset file was not found!")
    print("Please place Telco-Customer-Churn.csv inside the data folder.")
else:
    print("\nDataset found! Loading data...")

    df = pd.read_csv(DATA_FILE)

    print("\nDataset loaded successfully!")
    print("Number of customers:", len(df))
    print("Number of columns:", len(df.columns))

    print("\nFirst 5 rows:")
    print(df.head().to_string())

    print("\nColumn names:")
    print(df.columns.tolist())

    print("\nChurn distribution:")
    print(df["Churn"].value_counts().to_string())

    print("\nMissing values:")
    print(df.isnull().sum().to_string())

    print("\nMonthly charges summary:")
    print(df["MonthlyCharges"].describe().to_string())

print("\nProgram finished.")
