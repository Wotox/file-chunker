from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import logging
import zipfile
import io

import source.main as chunker

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

@app.get("/")
async def root():
    return {"route": "root"}

@app.post("/divide/")
async def divide(chunk_size: int = Form(...),
                 file_name: str = Form(...), 
                 file: UploadFile = File(...)
                 ) -> StreamingResponse:
    
    logger.info('Processing file (chunking)')

    file_bytes = file.file.read()
    chunks_bytes = chunker.divide(file_bytes, chunk_size, file_name)
    
    zip_data = io.BytesIO()
    with zipfile.ZipFile(zip_data, mode='w') as zipd:
        for file, name in chunks_bytes:
            zipd.writestr(name, file)
    zip_data.seek(0)

    return StreamingResponse(zip_data, media_type='application/zip', headers={"Content-Disposition":f"attachment; filename={file_name}.zip"})

@app.post("/build/")
async def build(file: UploadFile = File(...)) -> StreamingResponse:
    logger.info('Processing file (building)')
    zip_file_name = file.filename
    file_bytes = file.file.read()
    
    file_bytes_io = io.BytesIO(file_bytes)
    with zipfile.ZipFile(file_bytes_io, 'r') as zip_ref:
        files_in_memory = {}

        for file_name in zip_ref.namelist():
            with zip_ref.open(file_name) as file:
                files_in_memory[file_name] = file.read()

    file_build = chunker.build(files_in_memory)
    file_io = io.BytesIO()
    file_io.write(file_build)
    file_io.seek(0)

    file_name = zip_file_name # temporary, request for extension or find it in chunks

    return StreamingResponse(file_io, media_type='application/octet-stream', headers={"Content-Disposition":f"attachment; filename={file_name}"})