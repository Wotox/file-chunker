import logging
from natsort import natsorted

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_files_list_with_names(chunks:list, name:str) -> list:
    result = []

    for i in range(len(chunks)):
        chunk_file_name = f'{str(i)}.bin'
        result.append([chunks[i], chunk_file_name])
    
    return result # [bytes, name]

def split_string_into_parts(bytes_string:bytes, num_parts:int) -> list:
    part_length = len(bytes_string) // num_parts
    parts = [bytes_string[i:i+part_length] for i in range(0, len(bytes_string), part_length)]

    if len(parts) > num_parts:
        parts[-2] += parts[-1]
        parts.pop()

    return parts

def calculate_chunks(file_size:int, chunks_size:int) -> tuple:
    chunks_number = int(file_size/chunks_size)+1
    chunk_size = file_size/chunks_number
    return chunks_number, chunk_size

def divide(file_bytes:str, chunk_size:int, file_name:str = 'default'):
    file_size = len(file_bytes)
    logger.info(f'File size is {file_size} bytes')

    chunks_number, chunk_size = calculate_chunks(file_size, chunk_size)
    divided_bytes_chunks = split_string_into_parts(file_bytes, chunks_number)
    
    chunks = create_files_list_with_names(divided_bytes_chunks, file_name)

    logger.info(f'Divided into {str(chunks_number)} chunks')
    return chunks

def build(chunks_dict):
    bytes_string = bytes()
    chunks_list = {key: chunks_dict[key] for key in natsorted(chunks_dict)}

    for _, file_bytes in chunks_list.items():
        bytes_string += file_bytes

    return bytes_string