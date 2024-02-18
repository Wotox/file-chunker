import io
import zipfile
import filetype

def zip_files(files:list[bytes]) -> io.BytesIO:
    zip_data = io.BytesIO()
    with zipfile.ZipFile(zip_data, mode='w') as zipd:
        for file, name in files:
            zipd.writestr(name, file)
    zip_data.seek(0)

    return zip_data

def unzip_files(file:bytes) -> dict:
    file_bytes_io = io.BytesIO(file)
    with zipfile.ZipFile(file_bytes_io, 'r') as zip_ref:
        files_in_memory = {}

        for file_name in zip_ref.namelist():
            with zip_ref.open(file_name) as file:
                files_in_memory[file_name] = file.read()
    
    return files_in_memory

def get_file_type(file:bytes) -> str:
    file_ext = '.' + filetype.guess(file).extension
    if file_ext is None:
        file_ext = ''

    return file_ext