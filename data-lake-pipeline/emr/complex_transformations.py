from pyspark.sql import SparkSession
from pyspark.sql.functions import col, when, to_date, year, month, avg

# Create SparkSession
spark = SparkSession.builder.appName("ComplexETL").getOrCreate()

# Load data from S3
df = spark.read.parquet("s3://ecommerce-processed-zone/transactions/")

# transformations
df_transformed = df     .withColumn("order_date", to_date(col("timestamp")))     .withColumn("order_year", year(col("order_date")))     .withColumn("order_month", month(col("order_date")))     .withColumn("discounted_amount", when(col("discount") > 0, col("amount") * (1 - col("discount"))).otherwise(col("amount")))     .filter(col("status") == "completed")

# Group by customer and compute average spend
agg_df = df_transformed.groupBy("customer_id", "order_year", "order_month")     .agg(avg("discounted_amount").alias("avg_monthly_spend"))

# Save to analytics zone
agg_df.write.mode("overwrite").partitionBy("order_year", "order_month")     .parquet("s3://ecommerce-analytics-zone/monthly_customer_spend/")