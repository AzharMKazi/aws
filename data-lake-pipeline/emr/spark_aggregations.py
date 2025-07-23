from pyspark.sql import SparkSession

# Initialize Spark session
spark = SparkSession.builder.appName("EMR Aggregations").getOrCreate()

# Load processed data from S3
df = spark.read.parquet("s3://ecommerce-processed-zone/transactions/")

# Aggregate example: total sales per product
agg_df = df.groupBy("product_id").sum("amount")

# Save results to analytics zone
agg_df.write.mode("overwrite").parquet("s3://ecommerce-analytics-zone/sales_summary/")