import os
import boto3
from botocore.client import Config

class AWSStorageHandler:

    def __init__(self, bucket_name, access_key=None, secret_key=None, prefix=None, *args, **kwargs):
        self.bucket_name = bucket_name
        self.client = boto3.client("s3",
                                aws_access_key_id=access_key,
                                aws_secret_access_key=secret_key,
                                config=Config(signature_version='s3v4'))
        self.prefix = prefix
    
    def upload(self, oid: str):
        expiration = 3600
        upload_url = self._get_signed_url(self.prefix, oid, method='put_object', expires_in=expiration)
        return upload_url, expiration

    def download(self, oid: str):
        expiration = 3600
        download_url = self._get_signed_url(self.prefix, oid, expires_in=expiration)
        return download_url, expiration


    def _get_signed_url(self, prefix: str, oid: str, expires_in: int, method: str = 'get_object') -> str:
        return self.client.generate_presigned_url(ClientMethod=method,
                                                Params={'Bucket': self.bucket_name,
                                                        'Key': os.path.join(prefix, oid) if prefix else oid},
                                                ExpiresIn=expires_in)
    
    def verify_large_file(self, oid: str):
        try:
            self.client.head_object(Bucket=self.bucket_name, Key=os.path.join("test", oid))
            return {"exist": True}
        except:
            return {"exist": False}


    def lock_large_file(self, oid: str):
        try:
            response = self.client.head_object(Bucket=self.bucket_name, Key=oid)
            if response.get("Metadata", {}).get("locked") == "True":
                return {"error": "File is already locked"}
            self.client.copy_object(Bucket=self.bucket_name, CopySource={"Bucket": self.bucket_name, "Key": oid},
                                    Key=oid, Metadata={"locked": "True"}, MetadataDirective="REPLACE")
            return {"message": "File is now locked"}
        except:
            return {"error": "File not found"}
    

    def unlock_large_file(self, oid: str):
        try:
            response = self.client.head_object(Bucket=self.bucket_name, Key=oid)
            if response.get("Metadata", {}).get("locked") == "False":
                return {"error": "File is already unlocked"}
            self.client.copy_object(Bucket=self.bucket_name, CopySource={"Bucket": self.bucket_name, "Key": oid},
                                    Key=oid, Metadata={"locked": "False"}, MetadataDirective="REPLACE")
            return {"message": "File is now unlocked"}
        except:
            return {"error": "File not found"}

