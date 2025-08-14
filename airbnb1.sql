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
  





  





