import pandas as pd

# Load the dataset
df = pd.read_csv("car_data1/Car_sales.csv")  # adjust filename if different

# Basic inspection
print("Shape of dataset:", df.shape)
print("\nColumn names:", df.columns.tolist())
print("\nFirst 5 rows:")
print(df.head())

print("\nData Info:")
print(df.info())

print("\nMissing values per column:")
print(df.isnull().sum())

print("\nSummary statistics (numerical columns):")
print(df.describe())

