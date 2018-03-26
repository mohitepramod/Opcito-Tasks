import boto3

iam = boto3.resource('iam')
iam.create_user(UserName = 'Test-PM')