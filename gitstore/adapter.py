from typing import Dict

from parse import upload, download

class ExternalAdapter:

    def upload_from_adapter(self, oid: str = None, size = None) -> Dict:
        response = {"oid": oid, "size": size}
        response.update(upload(oid).dict())
        if dict(response.get('actions', {})).get('upload'):
            response['authenticated'] = True
            headers = {}
            response['actions']['verify'] = {  
                "href": f"http:localhost:8080/verify/{oid}",
                "header": headers,
                "expires_in": 3600
            }

        return response

    def download_from_adapter(self, oid: str, size: int) -> Dict:
        response = {"oid": oid,
                    "size": size}
        response.update(dict(download(oid).dict()))
        if dict(response.get('actions', {})).get('download'): 
            response['authenticated'] = True
        return response
