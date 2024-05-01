import boto3

# Replace with your AWS credentials and bucket name
s3 = boto3.client(
    's3',
    aws_access_key_id='AKIAW3MEFO2MWQSHHA74',
    aws_secret_access_key='GdmWJwQT6wKDDyW/DfcwOaEVUOzKSfUiqO+D21tq',
    
)
bucket_name = 'todobuckets3'

try:
  # Attempt to list objects in your bucket (simple check)
  response = s3.list_objects_v2(Bucket=bucket_name)
  print("S3 Connection Successful!")
except Exception as e:
  print("S3 Connection Error:", e)
