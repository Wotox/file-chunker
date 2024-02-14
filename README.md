# file-chunker
1. The program can divide any file into equally-sized chunks.
2. The program can build any file using its chunks.

## Usage
### Chunking
Arguments: -d(--divide) path_to_file chunk_size(KB)\
Example: ```python main.py -d /path/to/file.bin 1000```
### Building
Arguments: -b(--build) path_to_chunks build_folder filename\
Example: ```python main.py -b /path/to/chunks /path/to/build file.bin```

---
Note: dividing large files into extremely small chunks (100MB into 10KB parts, for instance) will make this script crawl.
