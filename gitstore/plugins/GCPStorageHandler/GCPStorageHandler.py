import os
from google.cloud import storage

class GCPStorageHandler:
    def __init__(self):
        self.bucket_name = os.environ.get("BUCKET_NAME")
        self.client = storage.Client.from_service_account_json(os.environ.get("GOOGLE_APPLICATION_CREDENTIALS"))
        self.bucket = self.client.bucket(self.bucket_name)
    
    async def upload_large_file(self, file):
        blob = self.bucket.blob(file.filename)
        blob.upload_from_file(file.file)
        return {"oid": file.filename}
    
    def download_large_file(self, oid: str):
        blob = self.bucket.blob(oid)
        return blob.download_as_string()
    
    def delete_large_file(self, oid: str):
        blob = self.bucket.blob(oid)
        blob.delete()
        
    def verify_large_file(self, oid: str):
        blob = self.bucket.blob(oid)
        return {"exist": blob.exists()}