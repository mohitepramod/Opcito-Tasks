# Creating s3 bucket and uploading data to it,Managing permissions on bucket,deleting bucket.
import boto3
import botocore
import parser
import argparse


parser = argparse.ArgumentParser()

parser.add_argument("--bucketName")
parser.add_argument("--fileName")
parser.add_argument("--filePath")
args = parser.parse_args()

bucketName = args.bucketName
fileName = args.fileName
filePath = args.filePath
s3 = boto3.resource('s3')


class s3BucketOperations(object):

    def createS3Bucket(self):
        '''Creating s3 bucket'''

        s3.create_bucket(Bucket=bucketName)
        #s3.create_bucket(Bucket= bucketName, CreateBucketConfiguration={
        # 'LocationConstraint': 'us-east-1'})
        print "Bucket Created Successfully with name "+bucketName

    def uploadFileToS3(self):
        '''Upload file to s3 bucket'''

        s3.Object(bucketName, fileName).put(Body=open(filePath+fileName, 'rb'))

    def deleteBucket(self):
        '''Delete Bucket with it's content'''

        bucket = s3.Bucket(bucketName)
        for dataKey in bucket.objects.all():
            dataKey.delete()
        s3.delete()

    def accessToBucket(self):
        bucket = s3.Bucket(bucketName)
        exists = True
        bucket.Acl().put(ACL='public-read')
        #bucket.obj.Acl().put(ACL='public-read')
        print "Public-read  permissions set "
        try:
            s3.meta.client.head_bucket(Bucket=bucketName)
            print "Access is granted to bucket !!!"
        except botocore.exceptions.ClientError as e:
            # If a client error is thrown, then check that it was a 404 error.
            # If it was a 404 error, then the bucket does not exist.
            error_code = int(e.response['Error']['Code'])
            if error_code == 404:
                exists = False

        # managing cross-region replication configuration

        cors = bucket.Cors()

        config = {
            'CORSRules': [
                {
                    'AllowedMethods': ['GET'],
                    'AllowedOrigins': ['*']
                }
            ]
        }
        cors.put(CORSConfiguration=config)
        cors.delete()


if __name__ == '__main__':
    bucketClassInstance = s3BucketOperations()
    #bucketClassInstance.createS3Bucket()
    #bucketClassInstance.uploadFileToS3()
    #bucketClassInstance.deleteBucket()    # don't run this...Because it's having lot more important data.
    bucketClassInstance.accessToBucket()