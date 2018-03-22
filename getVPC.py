# Getting VPC Info and creating Security Group inside that vpc

import json
import boto3

ec2 = boto3.resource('ec2', region_name='us-east-1')
client = boto3.client('ec2')

filters = [{'Name':'tag:Name', 'Values':['VPC-*']}]
vpcs = list(ec2.vpcs.filter(Filters=filters))

for vpc in vpcs:
    response = client.describe_vpcs(
        VpcIds=[
            vpc.id,
        ]
    )
    print "VPC Id" + vpc.id

ec2.create_security_group(GroupName="NewSG-PM",
                              Description="SecurityGroup-PM",
                              VpcId=vpc.id)
