import pandas as pd
import os

DATA_DIRECTORY = "./data"
OUTPUT_FILE_PATH = "./output/output.csv"

os.makedirs("./output", exist_ok=True)

all_rows = []

# Loop through CSVs
for file_name in os.listdir(DATA_DIRECTORY):
    if file_name.endswith(".csv"):
        df = pd.read_csv(f"{DATA_DIRECTORY}/{file_name}")

        # Normalize column names to lowercase
        df.columns = [c.lower() for c in df.columns]

        # Ensure required columns exist
        if not {"product", "price", "quantity", "date", "region"}.issubset(df.columns):
            print(f"Skipping {file_name}, missing columns: {df.columns}")
            continue

        # Filter for Pink Morsel
        df = df[df["product"].str.lower() == "pink morsel"]

        # Clean price column
        df["price"] = df["price"].replace("[\$,]", "", regex=True).astype(float)

        # Compute sales
        df["sales"] = df["price"] * df["quantity"]

        all_rows.append(df[["sales", "date", "region"]])

# Concatenate everything
if all_rows:
    final_df = pd.concat(all_rows)
    final_df = final_df.sort_values(by=["date", "region"])
    final_df.to_csv(OUTPUT_FILE_PATH, index=False)
    print(f"✅ Cleaned & sorted output saved to {OUTPUT_FILE_PATH}")
else:
    print("⚠️ No valid data processed. Check your input files.")
