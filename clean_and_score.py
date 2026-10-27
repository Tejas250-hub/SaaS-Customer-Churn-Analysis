
import pandas as pd
from pathlib import Path

# 1. Set up file locations
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
REPORT_DIR = BASE_DIR / "reports"

INPUT_FILE = DATA_DIR / "Telco-Customer-Churn.csv"
CLEAN_FILE = DATA_DIR / "cleaned_customers.csv"
RISK_FILE = REPORT_DIR / "churn_risk_output.csv"

print("=" * 50)
print("SAAS CHURN: DATA CLEANING AND RISK SCORING")
print("=" * 50)

# 2. Check that the dataset exists
if not INPUT_FILE.exists():
    raise FileNotFoundError(
        f"Dataset not found: {INPUT_FILE}"
    )

# 3. Load the dataset
df = pd.read_csv(INPUT_FILE)
df.columns = df.columns.str.strip()

print(f"\nOriginal records: {len(df)}")

# 4. Remove duplicate customer records
if "customerID" in df.columns:
    df = df.drop_duplicates(subset="customerID")
else:
    df = df.drop_duplicates()

print(f"Records after removing duplicates: {len(df)}")

# 5. Clean numeric columns
numeric_columns = [
    "tenure",
    "MonthlyCharges",
    "TotalCharges"
]

for column in numeric_columns:
    if column in df.columns:
        df[column] = pd.to_numeric(
            df[column], errors="coerce"
        )

# Missing TotalCharges may occur for new customers.
# Fill missing values using monthly charges * tenure.
if "TotalCharges" in df.columns:
    estimated_total = (
        df["MonthlyCharges"] * df["tenure"]
    )
    df["TotalCharges"] = (
        df["TotalCharges"].fillna(estimated_total)
    )

# Fill any remaining numeric missing values with
# the median of that column.
for column in numeric_columns:
    if column in df.columns:
        if df[column].isna().any():
            median_value = df[column].median()
            df[column] = df[column].fillna(median_value)

# 6. Check and correct invalid numeric values
if "tenure" in df.columns:
    df["tenure"] = df["tenure"].clip(lower=0, upper=1000)

if "MonthlyCharges" in df.columns:
    df["MonthlyCharges"] = df["MonthlyCharges"].clip(lower=0)

if "TotalCharges" in df.columns:
    df["TotalCharges"] = df["TotalCharges"].clip(lower=0)

# 7. Prepare churn labels
if "Churn" not in df.columns:
    raise ValueError("The dataset must contain a Churn column.")

df["Churn"] = (
    df["Churn"]
    .astype("string")
    .str.strip()
    .str.title()
)

# 8. Create churn-risk score
# This is a rule-based score, not a trained ML model.
df["RiskScore"] = 0

# Short tenure can indicate an early-stage customer
df.loc[df["tenure"] <= 12, "RiskScore"] += 30

# Month-to-month customers have less contract commitment
if "Contract" in df.columns:
    df.loc[
        df["Contract"].eq("Month-to-month"),
        "RiskScore"
    ] += 30

# Lack of tech support may indicate a support gap
if "TechSupport" in df.columns:
    df.loc[
        df["TechSupport"].eq("No"),
        "RiskScore"
    ] += 15

# Lack of online security is another possible risk signal
if "OnlineSecurity" in df.columns:
    df.loc[
        df["OnlineSecurity"].eq("No"),
        "RiskScore"
    ] += 15

# Higher monthly charges receive a modest risk weight
if "MonthlyCharges" in df.columns:
    high_charge_cutoff = df["MonthlyCharges"].median()
    df.loc[
        df["MonthlyCharges"] > high_charge_cutoff,
        "RiskScore"
    ] += 10

# Maximum possible score is 100
df["RiskScore"] = df["RiskScore"].clip(0, 100)

# 9. Assign risk categories
df["RiskLevel"] = pd.cut(
    df["RiskScore"],
    bins=[-1, 29, 59, 100],
    labels=["Low", "Medium", "High"]
).astype("string")

# 10. Save the cleaned dataset
DATA_DIR.mkdir(parents=True, exist_ok=True)
REPORT_DIR.mkdir(parents=True, exist_ok=True)

df.to_csv(CLEAN_FILE, index=False)

# 11. Save a separate customer risk report
risk_columns = [
    column for column in [
        "customerID",
        "tenure",
        "Contract",
        "MonthlyCharges",
        "TotalCharges",
        "Churn",
        "RiskScore",
        "RiskLevel"
    ]
    if column in df.columns
]

risk_df = df[risk_columns].sort_values(
    by="RiskScore", ascending=False
)

risk_df.to_csv(RISK_FILE, index=False)

# 12. Display results
print("\nData cleaning completed!")
print("Cleaned dataset:", CLEAN_FILE)
print("Risk report:", RISK_FILE)

print("\nRisk category counts:")
print(df["RiskLevel"].value_counts().to_string())

print("\nAverage risk score:", round(df["RiskScore"].mean(), 2))

print("\nTop 10 customers by risk score:")
print(risk_df.head(10).to_string(index=False))

print("\nChurn distribution:")
print(df["Churn"].value_counts(dropna=False).to_string())

print("\nAll tasks completed successfully!")
