import boto3

def lambda_handler(event, context):
    """
    AWS Lambda function to trigger a Glue job on S3 file upload event.
    """
    glue = boto3.client('glue')
    job_name = 'clean-transactions'

    response = glue.start_job_run(JobName=job_name)
    return {
        'statusCode': 200,
        'body': f'Glue job started: {response["JobRunId"]}'
    }