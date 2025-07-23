#!/bin/bash
# Create necessary S3 buckets for data zones

aws s3 mb s3://ecommerce-raw-zone
aws s3 mb s3://ecommerce-processed-zone
aws s3 mb s3://ecommerce-analytics-zone