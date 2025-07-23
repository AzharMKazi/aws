provider "aws" {
  region = "us-east-1"
}

resource "aws_iam_role" "glue_role" {
  name = "glue-service-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [{
      Action = "sts:AssumeRole",
      Principal = {
        Service = "glue.amazonaws.com"
      },
      Effect = "Allow",
      Sid    = ""
    }]
  })
}

resource "aws_s3_bucket" "raw" {
  bucket = "ecommerce-raw-zone"
  force_destroy = true
}

resource "aws_s3_bucket" "processed" {
  bucket = "ecommerce-processed-zone"
  force_destroy = true
}

resource "aws_s3_bucket" "analytics" {
  bucket = "ecommerce-analytics-zone"
  force_destroy = true
}

resource "aws_iam_policy_attachment" "glue_s3_policy" {
  name       = "glue-s3-attach"
  roles      = [aws_iam_role.glue_role.name]
  policy_arn = "arn:aws:iam::aws:policy/AmazonS3FullAccess"
}

resource "aws_glue_job" "clean_transform" {
  name     = "clean-transactions"
  role_arn = aws_iam_role.glue_role.arn
  command {
    name            = "glueetl"
    script_location = "s3://ecommerce-raw-zone/scripts/clean_transform.py"
    python_version  = "3"
  }
  max_retries = 1
}

resource "aws_lambda_function" "trigger_glue" {
  filename         = "lambda_function_payload.zip"
  function_name    = "trigger_glue"
  role             = aws_iam_role.glue_role.arn
  handler          = "trigger_glue.lambda_handler"
  runtime          = "python3.9"
  source_code_hash = filebase64sha256("lambda/trigger_glue.py")
}