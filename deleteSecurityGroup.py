import boto3
from botocore.exceptions import ClientError
# Create EC2 client
ec2 = boto3.client('ec2')

# Delete security group
try:
    response = ec2.delete_security_group(GroupId='sg-676f2411')
    print('Security Group Deleted')
except ClientError as e:
    print(e)