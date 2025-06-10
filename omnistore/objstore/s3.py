import io
import os
from pathlib import Path

import boto3
from botocore.exceptions import ClientError

from omnistore.objstore.objstore import ObjStore


class S3(ObjStore):
    def __init__(self, bucket: str, endpoint: str = None):
        """
        Construct a new client to communicate with the AWS S3 provider.
        
        AWS credentials are expected to be provided via environment variables:
        - AWS_ACCESS_KEY_ID
        - AWS_SECRET_ACCESS_KEY
        - AWS_DEFAULT_REGION
        """
        region = os.environ.get("AWS_DEFAULT_REGION")
        
        # If a region is not specified, the bucket is created in the S3 default region (us-east-1).
        # If the user explicitly provides an endpoint_url, the region is not used.
        kwargs = {}
        if endpoint:
            kwargs['endpoint_url'] = endpoint
        if region:
            kwargs['region_name'] = region
        
        self.client = boto3.client('s3', **kwargs)
        self.resource = boto3.resource('s3', **kwargs)
        self.bucket_name = bucket

        # Make sure the bucket exists
        try:
            self.client.head_bucket(Bucket=bucket)
        except ClientError as e:
            # If bucket doesn't exist, create it
            if e.response['Error']['Code'] == '404':
                kwargs = {}
                # For non us-east-1 region, we need to specify the LocationConstraint parameter when creating the bucket
                if region:
                    kwargs['CreateBucketConfiguration'] = {
                        "LocationConstraint": region
                    }
                self.client.create_bucket(Bucket=bucket, **kwargs)
            else:
                raise e

    def create_dir(self, dirname: str):
        if not dirname.endswith("/"):
            dirname += "/"
        empty_stream = io.BytesIO(b"")
        self.client.put_object(Bucket=self.bucket_name, Key=dirname, Body=empty_stream)

    def delete_dir(self, dirname: str):
        if not dirname.endswith("/"):
            dirname += "/"
        
        bucket = self.resource.Bucket(self.bucket_name)
        bucket.objects.filter(Prefix=dirname).delete()

    def upload(self, src: str, dest: str):
        self.client.upload_file(src, self.bucket_name, dest)

    def upload_dir(self, src_dir: str, dest_dir: str):
        for file in Path(src_dir).rglob("*"):
            if file.is_file():
                dest_path = f"{dest_dir}/{file.relative_to(src_dir)}"
                self.upload(str(file), dest_path)
            elif file.is_dir():
                self.create_dir(f"{dest_dir}/{file.relative_to(src_dir)}/")

    def download(self, src: str, dest: str):
        self.client.download_file(self.bucket_name, src, dest)

    def download_dir(self, src_dir: str, dest_dir: str):
        if not src_dir.endswith("/"):
            src_dir += "/"
        path = Path(dest_dir)
        if not path.exists():
            path.mkdir(parents=True)
            
        paginator = self.client.get_paginator('list_objects_v2')
        pages = paginator.paginate(Bucket=self.bucket_name, Prefix=src_dir)
        
        for page in pages:
            if 'Contents' not in page:
                continue
                
            for obj in page['Contents']:
                key = obj['Key']
                if key.endswith('/'):  # Skip directories
                    continue
                    
                file_path = Path(dest_dir, Path(key).relative_to(src_dir))
                if not file_path.parent.exists():
                    file_path.parent.mkdir(parents=True, exist_ok=True)
                    
                self.download(key, str(file_path))

    def delete(self, filename: str):
        self.client.delete_object(Bucket=self.bucket_name, Key=filename)

    def exists(self, filename: str):
        try:
            self.client.head_object(Bucket=self.bucket_name, Key=filename)
            return True
        except ClientError as e:
            if e.response['Error']['Code'] == '404':
                return False
            else:
                raise e
