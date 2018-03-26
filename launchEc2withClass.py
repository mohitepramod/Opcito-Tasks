import boto3
import parser
import json,requests
import argparse
import time
import datetime

parser = argparse.ArgumentParser()

parser.add_argument("--ImageId")
parser.add_argument("--SecurityGroupIds")
parser.add_argument("--MinCount")
parser.add_argument("--MaxCount")
parser.add_argument("--InstanceType")
parser.add_argument("--KeyName")
parser.add_argument("--SubnetId")
parser.add_argument("--VolumeSize")
parser.add_argument("--Tags")

args = parser.parse_args()

ImageId = args.ImageId
SecurityGroupIds = args.SecurityGroupIds
MinCount = args.MinCount
MaxCount = args.MaxCount
InstanceType = args.InstanceType
KeyName = args.KeyName
SubnetId = args.SubnetId
VolumeSize = args.VolumeSize
Tag = args.Tags


ec2 = boto3.resource('ec2')
client = boto3.client('ec2')

class LaunchEC2InstanceClass(object):

    def launchec2(self):

        ''' creating new ec2 instance and create new volume and attach the same volume to created instance.'''

        instance = ec2.create_instances(ImageId=ImageId,\
                                        MinCount=int(MinCount),\
                                        MaxCount=int(MaxCount),\
                                        InstanceType=InstanceType, \
                                        BlockDeviceMappings=[
                                            {
                                                "DeviceName": "/dev/sdf",
                                                "VirtualName": "ephemeral0",
                                                "Ebs": {
                                                    "Encrypted": False,
                                                    "Iops": 123,
                                                    "DeleteOnTermination": True,
                                                    "VolumeSize": int(VolumeSize),
                                                    "VolumeType": "io1"
                                                }
                                            },
                                        ],
                                        tag=client.create_tags(
                                            DryRun= False,
                                            Tags=[
                                                {
                                                    'Key': 'Name',
                                                    'Value': 'Test-Instance-PM'
                                                },
                                            ]
                                        )
                                        )


        print "Success !!!"

    def createSecurityGroup(self):

        ''' Create New security group inside vpc with inbound and outound rules'''

        vpc_response = client.describe_vpcs()
        vpc_id = vpc_response.get('Vpcs', [{}])[0].get('VpcId', '')
        response = ec2.create_security_group(GroupName= "SECURITY_GROUP_NAME",
                                         Description= "DESCRIPTION",
                                         VpcId=vpc_id)
        securityGroupId = response['GroupId']
        data = ec2.authorize_security_group_ingress(
            GroupId=securityGroupId,
            IpPermissions=[
                {'IpProtocol': 'tcp',
                 'FromPort': 80,
                 'ToPort': 80,
                 'IpRanges': [{'CidrIp': '0.0.0.0/0'}]},
                {'IpProtocol': 'tcp',
                 'FromPort': 22,
                 'ToPort': 22,
                 'IpRanges': [{'CidrIp': '0.0.0.0/0'}]}
            ])
        print('Ingress Successfully Set %s' % data)


    def deleteSecurityGroup(self):

        '''Deleting Security group by using security group Id'''

        response = client.delete_security_group(GroupId='')
        print "Security group deleted successfully !!!"


    def getVpcDetails(self):

        '''Getting VPC details by specifying filter on name of vpc and getting VpcId'''

        filters = [{'Name': 'tag:Name', 'Values': ['VPC-*']}]
        vpcs = list(ec2.vpcs.filter(Filters=filters))

        for vpc in vpcs:
            response = client.describe_vpcs(
                VpcIds=[
                    vpc.id,
                ]
            )
            print "VPC Id" + vpc.id

    def createVPC(self):

        '''Creating new VPC '''

        response = client.create_vpc(
            CidrBlock='10.0.0.0/16',
            AmazonProvidedIpv6CidrBlock= False,
            DryRun=False,
            InstanceTenancy= "default"
        )
        response.wait_until_available()
        print "Response code from VPC:"+response.id

    def getRunningInstanceId(self):

        '''Getting instance id by applying filter '''

        instances = ec2.instances.filter(
            Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])
        for instance in instances:
            print(instance.id, instance.instance_type)



if __name__=='__main__':
    launchInstance = LaunchEC2InstanceClass()
    #launchInstance.launchec2()
    #launchInstance.getRunningInstanceId()
    #launchInstance.createSecurityGroup()
    #launchInstance.deleteSecurityGroup()
    #launchInstance.getVpcDetails()
    launchInstance.createVPC()