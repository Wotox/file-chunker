import os
import sys
import logging
from pathlib import Path
from natsort import natsorted

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_file_from_bytes_string(bytes_string:list, path:str, file_name):
    Path(path).mkdir(parents=True, exist_ok=True)
    file_path = path + '/' + file_name

    with open(file_path, 'wb') as file:
        file.write(bytes_string)

def create_files_from_string_chunks(chunks:list, name:str):
    chunks_path = 'output' + '/' + name + '/'
    Path(chunks_path).mkdir(parents=True, exist_ok=True)

    for i in range(len(chunks)):
        chunk_file_name = f'{str(i)}.chunk'
        chunk_file_path = chunks_path + chunk_file_name

        with open(chunk_file_path, 'wb') as file:
                file.write(chunks[i])

def split_string_into_parts(bytes_string, num_parts):
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

def read_file_contents(path:str) -> str:
    """Returns a string with byte content"""
    with open(path, 'rb') as file:
        file_contents = file.read()

    return file_contents

def divide(file_path:str, chunk_size:int):
    file_name = os.path.split(file_path)[-1]
    file_size = os.stat(file_path)[6]
    logger.info(f'File size is {file_size} bytes')

    byte_representation = read_file_contents(file_path)
    chunks_number, chunk_size = calculate_chunks(file_size, chunk_size)
    divided_bytes_chunks = split_string_into_parts(byte_representation, chunks_number)
    
    create_files_from_string_chunks(divided_bytes_chunks, file_name)

    logger.info(f'Divided into {str(chunks_number)} chunks')

def build(chunks_path, build_path, file_name):
    bytes_string = bytes()
    files = natsorted(os.listdir(chunks_path))

    for file in files:
        file_content = read_file_contents(chunks_path + '/' + file)
        bytes_string += file_content

    create_file_from_bytes_string(bytes_string, build_path, file_name)

def main():
    arguments = sys.argv[1:]
    if not arguments:
        print('1. Mode: -d, --divide\nFile path: /files/file.txt\nChunk size: 1000')
        print('2. Mode: -b, --build\nChunks path: /chunks/document_chunks\nBuild folder: /built/document\nBuild file name: file.txt')
        return 0
    mode = arguments[0]
    if mode == '-d' or mode == '--divide':
        file = arguments[1]
        size = int(arguments[2])
        divide(file, size)
    elif mode == '-b' or mode == '--build':
        chunks_path = arguments[1]
        build_path = arguments[2]
        file_name = arguments[3]
        build(chunks_path, build_path, file_name)
    
    return 0

if __name__ == '__main__':
    main()