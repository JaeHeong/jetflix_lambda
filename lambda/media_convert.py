import glob
import json
import os
import uuid
import boto3
import datetime
import random
import ast

from botocore.client import ClientError

def lambda_handler(event, context):
    print(event)
    # event_json=ast.literal_eval(event['Records'][0]['body'])['Message']
    # event=json.loads(json.loads(event['Records'][0]['body'])['Message'])
    event=json.loads(event['Records'][0]['body'])
    assetID=str(uuid.uuid4())
    sourceS3Bucket=event['Records'][0]['s3']['bucket']['name']
    sourceS3Key=event['Records'][0]['s3']['object']['key']
    sourceS3='s3://'+sourceS3Bucket+'/'+sourceS3Key
    print(os.path.dirname(sourceS3).split('/')[-1]+'/'+os.path.splitext(os.path.basename(sourceS3))[0])
    if os.path.splitext(os.path.basename(sourceS3))[-1] != ".mp4":
        return {
            'statusCode':200,
            'body':'This is not video file',
            'headers':{'Content-Type':'application/json','Access-Control-Allow-Origin':'*'}
        }
    # sourceS3Basename=os.path.splitext(os.path.basename(sourceS3))[0]
    sourceS3Basename=os.path.dirname(sourceS3).split('/')[-1]+'/'+os.path.splitext(os.path.basename(sourceS3))[0]
    destinationS3='s3://'+os.environ['DestinationBucket']
    destinationS3basename=os.path.splitext(os.path.basename(destinationS3))[0]
    mediaConvertRole=os.environ['MediaConvertRole']
    region=os.environ['AWS_DEFAULT_REGION']
    statusCode=200
    body={}
    
    jobMetadata={'assetID':assetID}
    
    print(json.dumps(event))
    
    try:
        with open('job.json') as json_data:
            jobSettings=json.load(json_data)

            
        mc_client=boto3.client('mediaconvert',region_name=region)
        endpoints=mc_client.describe_endpoints()
        
        client=boto3.client('mediaconvert',region_name=region,endpoint_url=endpoints['Endpoints'][0]['Url'],verify=False)
        
        jobSettings['Inputs'][0]['FileInput']=sourceS3
        S3KeyHLS=sourceS3Basename
        print(S3KeyHLS)
        jobSettings['OutputGroups'][0]['OutputGroupSettings']['HlsGroupSettings']['Destination']=destinationS3+'/'+S3KeyHLS
        
        print('jobSettings: ')
        print(json.dumps(jobSettings))
        
        job=client.create_job(Role=mediaConvertRole,UserMetadata=jobMetadata,Settings=jobSettings)
        print(json.dumps(job,default=str))
        
    except Exception as e:
        print('Exception: %s' % e)
        statusCode=500
        raise
    finally:
        return{
            'statusCode':statusCode,
            'body':json.dumps(body),
            'headers':{'Content-Type':'application/json','Access-Control-Allow-Origin':'*'}
        }
