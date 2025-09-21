import pandas as pd

# Load dataset
df = pd.read_csv("car_data1/Car_sales.csv")

# 1. Standardize column names (remove spaces, make lowercase)
df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

print("Cleaned column names:", df.columns.tolist())

# 2. Handle missing values
# Drop rows where sales data is missing
df = df.dropna(subset=["sales_in_thousands"])

# Fill missing numerical values (e.g., price) with median
if "price_in_thousands" in df.columns:
    df["price_in_thousands"] = df["price_in_thousands"].fillna(df["price_in_thousands"].median())

# 3. Convert data types (if any numerical column is read as string)
for col in ["sales_in_thousands", "price_in_thousands"]:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

# 4. Save the cleaned dataset
df.to_csv("car_data1/Car_sales_cleaned.csv", index=False)

print("\nData cleaned and saved as 'Car_sales_cleaned.csv'")
print("Shape after cleaning:", df.shape)
print("Missing values left:\n", df.isnull().sum())
