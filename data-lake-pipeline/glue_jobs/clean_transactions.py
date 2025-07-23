import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job

# Glue boilerplate
args = getResolvedOptions(sys.argv, ['JOB_NAME'])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# Load raw data from S3
raw_data = glueContext.create_dynamic_frame.from_catalog(database="ecommerce", table_name="transactions_raw")

# Simple transformation
cleaned_data = raw_data.drop_fields(['redundant_column'])

# Save cleaned data
glueContext.write_dynamic_frame.from_options(
    frame=cleaned_data,
    connection_type="s3",
    connection_options={"path": "s3://ecommerce-processed-zone/transactions/"},
    format="parquet"
)

job.commit()