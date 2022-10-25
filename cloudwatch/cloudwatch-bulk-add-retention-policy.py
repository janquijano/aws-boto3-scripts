import boto3


logs = boto3.client('logs')


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
            retentionInDays = 90
        )