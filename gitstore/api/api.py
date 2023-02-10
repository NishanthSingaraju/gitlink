from fastapi import FastAPI, UploadFile
from fastapi.responses import FileResponse
import yaml
from parse import get_storage_handler

app = FastAPI()

def load_config(file_path):
    with open(file_path, 'r') as f:
        config = yaml.safe_load(f)
    return config

@app.post("/update_config")
async def update_config(file: UploadFile):
    with open('config.yaml', 'wb') as f:
        f.write(await file.read())
    return {'message': 'Config updated successfully'}

@app.post("/objects/batch")
async def get_batch_object(operation, oid):
    config = load_config('config.yaml')
    storage_handler = get_storage_handler(config)
    if operation == "upload":
        return storage_handler.upload(oid)
    elif operation == "download":
        return storage_handler.download(oid)
    else:
        raise ValueError("Invalid paramter input")

@app.delete("/objects/{oid}/delete")
def delete_large_file(oid: str):
    config = load_config('config.yaml')
    storage_handler = get_storage_handler(config)
    return storage_handler.delete_large_file(oid)

@app.post("/locks/{oid}/lock")
async def lock_large_file(oid: str):
    config = load_config('config.yaml')
    storage_handler = get_storage_handler(config)
    return await storage_handler.lock_large_file(oid)

@app.post("/locks/{oid}/unlock")
async def unlock_large_file(oid: str):
    config = load_config('config.yaml')
    storage_handler = get_storage_handler(config)
    return await storage_handler.unlock_large_file(oid)

@app.post("/locks/{oid}/lock")
async def lock_large_file(oid: str):
    config = load_config('config.yaml')
    storage_handler = get_storage_handler(config)
    return await storage_handler.lock_large_file(oid)

@app.post("/locks/{oid}/unlock")
async def unlock_large_file(oid: str):
    config = load_config('config.yaml')
    storage_handler = get_storage_handler(config)
    return await storage_handler.unlock_large_file(oid)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000, debug=True)