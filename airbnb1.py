# ------------------------------------------------------------
# Airbnb Data Analysis Project
# Author: Rithika R
# Description: Load, clean, analyze, and visualize Airbnb listings
# ------------------------------------------------------------

# Import libraries
import pandas as pd
from sqlalchemy import create_engine
import matplotlib.pyplot as plt
import seaborn as sns
from openpyxl import load_workbook

# Load data
df = pd.read_csv(r"C:\Users\rithi\OneDrive\Documents\fielsss\Airbin\Airbnb_Open_Data.csv",low_memory=False)

# Price cleaning (remove $ and commas, convert to float)
df['price']=(df['price'].astype(str).str.replace(r'[\$,]',"",regex=True).replace("",pd.NA).astype(float))

#Handling misssing values
df['price']=df['price'].fillna(df['price'].mean())

#Remove duplicates
df.drop_duplicates(inplace=True)

# Convert last_review to datetime (handle invalid formats)
df['last_reviewdate']=pd.to_datetime(df['last_review'],errors='coerce')

# Fill missing dates with earliest date in dataset (or could use today's date)
df['last_reviewdate']=df['last_reviewdate'].fillna(df['last_reviewdate'].min())

# ------------------------------------------------------------
# Feature Engineering
# ------------------------------------------------------------

# Extract month from last review date
df['month']=df['last_reviewdate'].dt.month


# Price Distribution (Remove Outliers for Clarity)

plt.figure(figsize=(10, 6))
sns.histplot(df[df['price'] < 500]['price'], bins=50, kde=True)
plt.title("Price Distribution of Airbnb Listings (< $500)")
plt.xlabel("Price (USD)")
plt.ylabel("Number of Listings")
plt.show()

#  Top 10 Most Expensive Neighborhoods
top_neighbourhoods = (
    df.groupby("neighbourhood")["price"]
    .median()
    .sort_values(ascending=False)
    .head(10)
)

plt.figure(figsize=(10, 6))
top_neighbourhoods.plot(kind="bar", color="skyblue")
plt.title("Top 10 Most Expensive Neighborhoods (Median Price)")
plt.ylabel("Median Price (USD)")
plt.xticks(rotation=45)
plt.show()

#  Monthly Review Trends
monthly_trend = (
    df.groupby('month')["id"]
    .count()
    .rename("listing_count")
)

plt.figure(figsize=(10, 6))
monthly_trend.plot(marker='o')
plt.title("Number of Listings Reviewed per Month")
plt.xlabel("Month")
plt.ylabel("Listings Reviewed")
plt.grid(True)
plt.show()

#  Price Correlation Heatmap
plt.figure(figsize=(8, 5))
numeric_cols = df.select_dtypes(include='number')
sns.heatmap(numeric_cols.corr(), annot=True, cmap="coolwarm", fmt=".2f")
plt.title("Correlation Heatmap")
plt.show()


# ------------------------------------------------------------
# Insights
# ------------------------------------------------------------
print("\n Key Insights:")
print("- Most listings are priced below $500; a few outliers skew the data.")
print("- The most expensive neighborhoods (median price) are concentrated in luxury areas.")
print("- There is a seasonal pattern in review activity, peaking around certain months.")
print("- Price is moderately correlated with number of reviews and availability.")



# --- MySQL Upload ---

try:
    engine = create_engine('mysql+pymysql://root:newpassword123@localhost/Airbnb_Data_Analysis_Project')

    df.to_sql('airbnb_listings', con=engine, if_exists='replace', index=False)

    print("Successfully uploaded to MySQL")

except Exception as e:
    print("Upload to MySQL failed!")
    print(f"Error: {e}")

df.to_excel("Airbnb_Open_Data.xlsx", sheet_name="New_Sheet", index=False)



