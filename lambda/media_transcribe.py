import json
import boto3
import os

s3_client = boto3.client('s3')
transcribe_client = boto3.client('transcribe')

def create_transcription_job(job_name, job_uri, output_bucket, object_id):
    response = transcribe_client.start_transcription_job(
        TranscriptionJobName=job_name,
        Media={'MediaFileUri': job_uri},
        OutputBucketName=output_bucket,
        OutputKey=f'{object_id}/',
        MediaFormat='mp4',
        # LanguageCode='auto',
        IdentifyLanguage=True,
        LanguageOptions=[ "ko-KR", "en-US", "ja-JP", "zh-CN"],
        Subtitles={'Formats': ['vtt', 'srt'], 'OutputStartIndex': 1}
    )
    
    return response

def lambda_handler(event, context):
    # event=json.loads(json.loads(event['Records'][0]['body'])['Message'])
    event=json.loads(event['Records'][0]['body'])
    record = event['Records'][0]
    bucket_name = record['s3']['bucket']['name']
    object_key = record['s3']['object']['key']
    sourceS3='s3://'+bucket_name+'/'+object_key
    object_id = object_key.split('/')[0]
    object_name = object_key.split('/')[1]
    if os.path.splitext(os.path.basename(sourceS3))[-1] != ".mp4":
        return {
            'statusCode':200,
            'body':'This is not video file',
            'headers':{'Content-Type':'application/json','Access-Control-Allow-Origin':'*'}
        }
    job_name = f'transcription-job-{object_id}-{object_name}'
    job_uri = f's3://{bucket_name}/{object_key}'
    output_bucket = 'db-transcribe'

    response = create_transcription_job(job_name, job_uri, output_bucket, object_id)
    print(f"Transcription job {job_name} has been started.")
    
    return {
        'statusCode': 200,
        'body': json.dumps('Transcription job has been started.')
    }
