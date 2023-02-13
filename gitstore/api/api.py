from fastapi import FastAPI, UploadFile, Body
from parse import get_storage_handler, upload, download, get_config
from schema import BatchRequest

app = FastAPI()

@app.post("/update_config")
async def update_config(file: UploadFile):
    with open('config.yaml', 'wb') as f:
        f.write(await file.read())
    return {'message': 'Config updated successfully'}

@app.get("/")
def root():
    return 

@app.post("/objects/batch")
async def batch(payload: BatchRequest = Body(...)): 
    for object in payload.objects:
        if payload.operation == "upload":
            return upload(object.oid)
        elif payload.operation == "download":
            return download(object.oid)
        else:
            raise ValueError("Invalid paramter input")

@app.delete("/objects/{oid}/delete")
def delete_large_file(oid: str):
    config = get_config()
    storage_handler = get_storage_handler(config)
    return storage_handler.delete_large_file(oid)

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