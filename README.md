# 🏠 Airbnb Data Analysis Project (End-to-End Pipeline)

## 📌 Project Overview
This project performs **Airbnb Listings Data Analysis** using:
- **SQL (MySQL)** → Data extraction & queries
- **Python (Pandas, Matplotlib, Seaborn)** → Data cleaning, feature engineering & analysis
- **Power BI** → Interactive dashboard for insights & pricing strategy recommendations

The goal is to provide **actionable insights** for pricing strategies, location targeting, and seasonal demand patterns.

---

## 📂 Dataset
**Source:** [Airbnb Open Data – Kaggle](https://www.kaggle.com/datasets/arianazmoudeh/airbnbopendata)  
**File:** `Airbnb_Open_Data.csv`  
**Columns Include:**
- `id`, `name`, `host_id`, `host_name`
- `neighbourhood_group`, `neighbourhood`
- `latitude`, `longitude`
- `room_type`, `price`, `minimum_nights`
- `number_of_reviews`, `last_review`, `reviews_per_month`
- `availability_365`

---

## 🛠 Tools & Technologies
- **SQL**: MySQL for data extraction
- **Python**: Pandas, Matplotlib, Seaborn for EDA
- **Power BI**: Dashboard creation & visualization
- **Excel**: Export of cleaned dataset

---

## 📊 SQL Analysis

```sql
-- Create database---------

CREATE DATABASE Airbnb_Data_Analysis_Project;
USE Airbnb_Data_Analysis_Project;

-- create table -----------

CREATE TABLE airbnb_listings (
    id INT PRIMARY KEY,
    name VARCHAR(255),
    host_id INT,
    host_name VARCHAR(100),
    neighbourhood_group VARCHAR(100),
    neighbourhood VARCHAR(100),
    latitude DECIMAL(10, 8),
    longitude DECIMAL(11, 8),
    room_type VARCHAR(50),
    price DECIMAL(10, 2),
    minimum_nights INT,
    number_of_reviews INT,
    last_review DATE,
    reviews_per_month DECIMAL(5, 2),
    calculated_host_listings_count INT,
    availability_365 INT
);

-- 1. Find Average Price by Location ----- 

SELECT 
    neighbourhood AS location,
    AVG(price) AS avg_price,
    COUNT(*) AS total_listings
FROM 
    airbnb_listings
GROUP BY 
    neighbourhood
ORDER BY 
    avg_price DESC;
    
-- 2. Most Popular Room Types -------- 

SELECT room_type,
COUNT(*) AS Total_listings,
AVG(price) AS average_price
FROM airbnb_listings
GROUP BY room_type
ORDER BY AVG(price) DESC;
    
-- 3. Price Trends by Season -----------
SELECT 
CASE 
   WHEN MONTH BETWEEN 1 AND 2 OR MONTH=12 THEN 'WINTER'
   WHEN MONTH BETWEEN 3 AND 5 THEN 'SPRING'
   WHEN MONTH BETWEEN 6 AND 8 THEN 'SUMMER'
   WHEN MONTH BETWEEN 9 AND 11 THEN 'FALL'
END AS SEASON,
AVG(price) AS averager_price
FROM(
 SELECT 
   EXTRACT(MONTH FROM
	CASE
          WHEN STR_TO_DATE(last_review, '%m/%d/%Y') IS NOT NULL 
           THEN STR_TO_DATE(last_review,'%m/%d/%Y')
        WHEN STR_TO_DATE(last_review, '%d-%m-%Y') IS NOT NULL 
          THEN STR_TO_DATE(last_review,'%d-%m-%Y')
        WHEN STR_TO_DATE(last_review, '%d/%m/%Y') IS NOT NULL 
          THEN STR_TO_DATE(last_review,'%d/%m/%Y')
        WHEN STR_TO_DATE(last_review, '%m-%d-%Y') IS NOT NULL 
          THEN STR_TO_DATE(last_review,'%m-%d-%Y')
        ELSE NULL
	END ) AS month,
       price
FROM airbnb_listings
WHERE last_review IS NOT NULL
) AS subquery
  GROUP BY SEASON
  ORDER BY MIN(month);
```
## 📊 Python Analysis
```python

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
```
## Python Visualization
### price distribution of airbnb listners <500
![price distribution of airbnb listners <500](<img width="1504" height="1003" alt="price distribution of airbnb listners" src="https://github.com/user-attachments/assets/a6b6ed49-45d9-4a49-81f5-547abc23fcde" />
### top 10 most expansive neighours
![top 10 most expansive neighours](<img width="1504" height="1003" alt="top 10 most expansive neighours" src="https://github.com/user-attachments/assets/72c63a37-6df5-4420-a3a9-59d3e9ba4fb9" />
### Number of listings reviews per month
![Number of listings reviews per month](<img width="1504" height="1003" alt="Number of listings reviews per month" src="https://github.com/user-attachments/assets/2bdbf95e-6a68-4f0d-8f45-451e5fa82729" />
### correlation heatmap
![correlation heatmap](<img width="1920" height="1008" alt="correlation heatmap" src="https://github.com/user-attachments/assets/8c70c6e8-4ec7-490d-95f5-ca1c4cd637ce" />

## PowerBI Dashboard
[PowerBI Link](https://rithikaramalingam3.wixsite.com/data-analyst-hub)

### Executive Summary
- KPIs: Total Listings, Avg Price, Highest Price, Review Score
- Map of listings by neighborhood
- Room type distribution
- Top 10 neighborhoods by avg price
![Executive Summary Dashboard](https://github.com/RithikaAnalyst/Airbnb_data_analysis_project/blob/main/dashboard%20(2).png)
### Most listings price under 500
![Most listings price under 500](https://github.com/RithikaAnalyst/Airbnb_data_analysis_project/blob/main/Most%20listings%20priced%20under%20%24500.png)
### KPIs
![KPIs](KPIs.png)


