import os
from google.cloud import storage

import datetime

class GCPStorageHandler:
    def __init__(self):
        self.bucket_name = os.environ.get("BUCKET_NAME")
        self.client = storage.Client.from_service_account_json(os.environ.get("GOOGLE_APPLICATION_CREDENTIALS"))
        self.bucket = self.client.bucket(self.bucket_name)
    
    async def upload(self, oid: str):
        blob = self.bucket.blob(oid)
        expiration = datetime.timedelta(hours=6)
        upload_url = blob.generate_signed_url(expiration=expiration, method="PUT")
        upload_url_expiry = datetime.datetime.now() + expiration
        return {
            "oid": oid,
            "actions": {
                "upload": {
                    "expires_at": upload_url_expiry,
                    "header": {"Content-Type": "application/octet-stream"},
                    "href": upload_url
                }
                },
            "authenticated": True
        }

    def download(self, oid: str):
        blob = self.bucket.blob(oid)
        expiration = datetime.timedelta(hours=6)
        download_url = blob.generate_signed_url(expiration=expiration, method="GET")
        download_url_expiry = datetime.datetime.now() + expiration
        return {
            "oid": oid,
            "actions": {
                "download": {
                "expires_at": download_url_expiry,
                "href": download_url
            }
            },
            "authenticated": True
        }
    
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