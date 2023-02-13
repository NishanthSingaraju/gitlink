from fastapi import FastAPI, UploadFile, Body
from parse import get_storage_handler, upload, download, get_config
from schema import BatchRequest

app = FastAPI()


@app.get("/")
def root():
    return 

@app.post("/update_config")
async def update_config(file: UploadFile):
    with open('config.yaml', 'wb') as f:
        f.write(await file.read())
    return {'message': 'Config updated successfully'}

@app.post("/objects/batch")
def batch(payload: BatchRequest = Body(...)):
    objects = []
    for obj in payload.objects:
        if payload.operation == "upload":
            objects.append(upload(obj.oid, obj.size))
        elif payload.operation == "download":
            objects.append(download(obj.oid, obj.size))
        else:
            raise ValueError("Invalid parameter input")
    return {"transfer": "basic", "authenticated": True, "objects": objects}


@app.get("/verify/{oid}")
def verify(oid: str):
    return True

@app.post("/upload/{oid}")
async def upload_file(oid: str, file: UploadFile):
    # Get the file's content
    file_content = await file.read()

    # Save the file to disk
    with open(f"../tester/files/{oid}", "wb") as f:
        f.write(file_content)
    return {"message": "File uploaded"}

@app.post("/locks/{oid}/lock")
async def lock_large_file(oid: str):
    config = get_config()
    storage_handler = get_storage_handler(config)
    return await storage_handler.lock_large_file(oid)

@app.post("/locks/{oid}/unlock")
async def unlock_large_file(oid: str):
    config = get_config()
    storage_handler = get_storage_handler(config)
    return await storage_handler.unlock_large_file(oid)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=True)