import boto3
import os
import logging


security_group_id = os.environ.get('SECURITY_GROUP_ID')
cidr_ip = os.environ.get('CIDR_OR_IP', "0.0.0.0/0")
from_port = int(os.environ.get('FROM_PORT', "22"))
to_port = int(os.environ.get('TO_PORT', "22"))
protocol = os.environ.get('PROTOCOL', "tcp")
logger = logging.getLogger()
level = logging.getLevelName(os.environ.get('LOG_LEVEL', 'INFO'))
logger.setLevel(level)

ec2 = boto3.client('ec2')


def lambda_handler(event, ctx):
    logger.info(event)

    security_group_id = event.get('security_group_id') or security_group_id

    try:
        response = ec2.revoke_security_group_ingress(
            GroupId = security_group_id,
            CidrIp = cidr_ip,
            FromPort = from_port,
            IpProtocol = protocol,
            ToPort = to_port,
            DryRun = False
            )
        logger.info(f"Remediation successful. SG ID: {security_group_id}")
    except Exception as e:
        logger.error(f"Failed to revoke security group rule. SG ID: {security_group_id}")
        raise(e)