import boto3
import parser
import argparse


parser = argparse.ArgumentParser()

parser.add_argument("--ImageId")
parser.add_argument("--SecurityGroupIds")
parser.add_argument("--MinCount")
parser.add_argument("--MaxCount")
parser.add_argument("--InstanceType")
parser.add_argument("--KeyName")
parser.add_argument("--SubnetId")

args = parser.parse_args()

ImageId = args.ImageId
SecurityGroupIds = args.SecurityGroupIds
MinCount = args.MinCount
MaxCount = args.MaxCount
InstanceType = args.InstanceType
KeyName = args.KeyName
SubnetId = args.SubnetId
print type(MinCount)
print type(int(MinCount))

print "ImageId :" +"'"+ImageId+"'"


ec2 = boto3.resource('ec2')

instance = ec2.create_instances(ImageId=ImageId,\
                                MinCount=int(MinCount),\
                                MaxCount=int(MaxCount),\
                                InstanceType=InstanceType\
                                )
print "Success !!!"