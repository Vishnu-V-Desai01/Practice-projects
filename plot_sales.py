
import os
import pandas as pd

DATA_DIR = "car_data1"
CLEANED_FILENAME = os.path.join(DATA_DIR, "Car_sales_cleaned.csv")
ORIGINAL_FILENAME = os.path.join(DATA_DIR, "Car_sales.csv")
PLOTS_DIR = "plots"

os.makedirs(PLOTS_DIR, exist_ok=True)

if os.path.exists(CLEANED_FILENAME):
    df = pd.read_csv(CLEANED_FILENAME)
    print(f"Loaded cleaned dataset: {CLEANED_FILENAME}")
elif os.path.exists(ORIGINAL_FILENAME):
    df = pd.read_csv(ORIGINAL_FILENAME)
    print(f"Loaded original dataset: {ORIGINAL_FILENAME}")
else:
    raise FileNotFoundError("No dataset found. Put Car_sales_cleaned.csv or Car_sales.csv in 'car_data1/'")

df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
print("Columns available:", df.columns.tolist())

possible_model_cols = ["model", "car_model", "car", "model_name", "name"]
possible_sales_cols = ["sales", "sales_in_thousands", "units_sold", "sold", "quantity", "sales_count"]

model_col = next((c for c in possible_model_cols if c in df.columns), None)
sales_col = next((c for c in possible_sales_cols if c in df.columns), None)

if model_col is None:
    model_col = next((c for c, t in df.dtypes.items() if t == "object"), None)
if sales_col is None:
    sales_col = next((c for c, t in df.dtypes.items() if pd.api.types.is_numeric_dtype(t)), None)

if model_col is None or sales_col is None:
    raise RuntimeError("Couldn't auto-detect model or sales columns. Please open the CSV and ensure there's a model/name and a numeric sales column.")

print(f"Using model column: '{model_col}' and sales column: '{sales_col}'")

df[sales_col] = (df[sales_col].astype(str)
                    .str.replace(r'[^\d\.-]', '', regex=True)
                    .replace('', '0')
                    .astype(float, errors='ignore')) 


df[sales_col] = pd.to_numeric(df[sales_col], errors="coerce").fillna(0)

model_sales = df.groupby(model_col)[sales_col].sum().sort_values(ascending=False)
top_n = 10
top_models = model_sales.head(top_n)

print("\nTop models (by sales):")
print(top_models)

import matplotlib.pyplot as plt

plt.figure(figsize=(12,6))
plt.bar(top_models.index.astype(str), top_models.values)
plt.xticks(rotation=45, ha='right')
plt.ylabel('Sales (units or value depending on your dataset)')
plt.title(f'Top {top_n} Car Models by Sales')
plt.tight_layout()
bar_path = os.path.join(PLOTS_DIR, f"top_{top_n}_bar.png")
plt.savefig(bar_path, dpi=150)
plt.close()
print(f"Saved Matplotlib bar chart: {bar_path}")

plt.figure(figsize=(8,8))
plt.pie(top_models.values, labels=top_models.index.astype(str), autopct='%1.1f%%', startangle=140)
plt.title(f'Sales distribution — Top {top_n} Models')
pie_path = os.path.join(PLOTS_DIR, f"top_{top_n}_pie.png")
plt.savefig(pie_path, dpi=150)
plt.close()
print(f"Saved Matplotlib pie chart: {pie_path}")

try:
    import plotly.express as px
    top_df = top_models.reset_index()
    top_df.columns = [model_col, 'sales']
    fig_bar = px.bar(top_df, x=model_col, y='sales', title=f'Top {top_n} Car Models (interactive)')
    bar_html = os.path.join(PLOTS_DIR, f"top_{top_n}_bar_plotly.html")
    fig_bar.write_html(bar_html, include_plotlyjs='cdn')
    print(f"Saved Plotly interactive bar chart: {bar_html}")
    fig_pie = px.pie(top_df, names=model_col, values='sales', title=f'Top {top_n} Sales Distribution')
    pie_html = os.path.join(PLOTS_DIR, f"top_{top_n}_pie_plotly.html")
    fig_pie.write_html(pie_html, include_plotlyjs='cdn')
    print(f"Saved Plotly interactive pie chart: {pie_html}")
except Exception as e:
    print("Plotly not available or failed to create interactive charts:", e)
    print("To enable Plotly charts: pip install plotly")

print("\nDone.")
