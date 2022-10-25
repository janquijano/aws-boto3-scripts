import boto3
import os


days_retention = os.environ.get('RETENTION_IN_DAYS', 90)
access_key = os.environ.get('ACCESS_KEY')
secret_key = os.environ.get('SECRET_KEY')
logs = boto3.client(
    'logs',
    aws_access_key_id = access_key,
    aws_secret_access_key = secret_key,
)


response = logs.describe_log_groups()
log_groups = response.get('logGroups')
next_token = response.get('nextToken')

while next_token is not None:
    response = logs.describe_log_groups(
        nextToken = next_token
    )
    log_groups = log_groups + response.get('logGroups')
    next_token = response.get('nextToken')


for log_group in log_groups:
    log_group_name = log_group.get('logGroupName')
    retention_in_days = log_group.get('retentionInDays')
    if retention_in_days is None:
        response = logs.put_retention_policy(
            logGroupName = log_group_name,
            retentionInDays = days_retention
        )
