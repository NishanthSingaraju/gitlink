import os
from google.cloud import storage
from google.oauth2 import service_account 
from datetime import timedelta

class GCPStorageHandler:
    def __init__(self, project_name, bucket_name, service_account_json, prefix = None, *args, **kwargs):
        self.bucket_name = bucket_name
        self.credentials = service_account.Credentials.from_service_account_file(
            os.path.basename(service_account_json)
        )
        self.client = storage.Client(project=project_name, credentials=self.credentials)
        self.bucket = self.client.bucket(self.bucket_name)
        self.prefix = prefix
    
    def upload(self, oid: str):
        expiration = 3600
        upload_url = self._get_signed_url(self.prefix, oid, http_method='PUT', expires_in=expiration)
        return upload_url, expiration

    def download(self, oid: str):
        expiration = 3600
        download_url = self._get_signed_url(self.prefix, oid, expires_in=expiration)
        return download_url, expiration


    def _get_signed_url(self, prefix: str, oid: str, expires_in: int, http_method: str = 'GET') -> str:
        if prefix is not None:
            blob = self.bucket.blob(os.path.join(prefix, oid))
        else: 
            blob = self.bucket.blob(oid)
        url = blob.generate_signed_url(expiration=timedelta(seconds=expires_in), method=http_method, version='v4',
                                            credentials=self.credentials)
        return url
        
    def verify_large_file(self, oid: str):
        blob = self.bucket.blob(os.path.join("test", oid))
        return {"exist": blob.exists()}
    
    def lock_large_file(self, oid: str):
        blob = self.bucket.blob(oid)
        if self.is_locked(oid):
            return {"error": "File is already locked"}
        blob.metadata = {"locked": "True"}
        blob.patch()
        return {"message": "File is now locked"}

    def unlock_large_file(self, oid: str):
        blob = self.bucket.blob(oid)
        if not self.is_locked(oid):
            return {"error": "File is already unlocked"}
        blob.metadata = {"locked": "False"}
        blob.patch()
        return {"message": "File is now unlocked"}

    def is_locked(self, oid: str):
        blob = self.bucket.blob(oid)
        return blob.metadata.get("locked", "False") == "True"