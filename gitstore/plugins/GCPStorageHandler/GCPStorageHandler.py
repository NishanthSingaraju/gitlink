import os
from google.cloud import storage
from google.oauth2 import service_account 

import datetime

class GCPStorageHandler:
    def __init__(self, project_name, bucket_name, service_account_json, *args, **kwargs):
        self.bucket_name = bucket_name
        self.credentials = service_account.Credentials.from_service_account_file(
            os.path.basename(service_account_json)
        )
        self.client = storage.Client(project=project_name, credentials=self.credentials)
        self.bucket = self.client.bucket(self.bucket_name)
    
    def upload(self, oid: str):
        blob = self.bucket.blob(oid)
        expiration = datetime.timedelta(hours=6)
        upload_url = blob.generate_signed_url(expiration=expiration, method="PUT")
        upload_url_expiry = datetime.datetime.now() + expiration
        print(upload_url)
        return upload_url, upload_url_expiry

    def download(self, oid: str):
        blob = self.bucket.blob(oid)
        expiration = datetime.timedelta(hours=6)
        download_url = blob.generate_signed_url(expiration=expiration, method="GET")
        download_url_expiry = datetime.datetime.now() + expiration
        return download_url, download_url_expiry

    def delete_large_file(self, oid: str):
        blob = self.bucket.blob(oid)
        blob.delete()
        
    def verify_large_file(self, oid: str):
        blob = self.bucket.blob(oid)
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