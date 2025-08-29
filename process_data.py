import pandas as pd
import glob

# Step 1: Get all CSV files from data folder
files = glob.glob("data/*.csv")

dfs = []

for file in files:
    # Step 2: Read each file
    df = pd.read_csv(file)
    
    # Step 3: Filter only Pink Morsel (case-insensitive)
    df = df[df["product"].str.lower() == "pink morsel"]
    
    # Step 4: Compute Sales (as numeric, rounded to 2 decimals)
    df["sales"] = (df["quantity"] * df["price"]).round(2)
    
    # Step 5: Keep only required columns
    df = df[["sales", "date", "region"]]
    
    dfs.append(df)

# Step 6: Combine all data
final_df = pd.concat(dfs)

# Step 7: Save to CSV
final_df.to_csv("data/processed_sales.csv", index=False)

print("✅ Processed file saved to data/processed_sales.csv")

