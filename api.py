from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import StreamingResponse
import logging
import io

from source.utils import zip_files, unzip_files, get_file_type
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
    zip_data = zip_files(chunks_bytes)

    return StreamingResponse(zip_data, media_type='application/zip', headers={"Content-Disposition":f"attachment; filename={file_name}.zip"})

@app.post("/build/")
async def build(file: UploadFile = File(...)) -> StreamingResponse:
    logger.info('Processing file (building)')
    
    file_name = file.filename
    file_bytes = file.file.read()
    
    files_in_memory = unzip_files(file_bytes)
    file_build = chunker.build(files_in_memory)
    file_io = io.BytesIO()
    file_io.write(file_build)
    file_io.seek(0)

    file_ext = get_file_type(file_build)
    if file_name[-4:len(file_name)] == '.zip':
        file_name = file_name[:-4] + file_ext
    else:
        file_name += file_ext

    return StreamingResponse(file_io, media_type='application/octet-stream', headers={"Content-Disposition":f"attachment; filename={file_name}"})