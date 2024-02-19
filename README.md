# file-chunker
1. The program can divide any file into equally-sized chunks.
2. The program can build any file using its chunks.

## Description
```divide``` accepts any file and returns zip compressed stream of its chunks that can be concatenated back together by capable program.\
```build``` accepts zipped archive of previously chunked file, puts it back together and returns its stream.
## Usage
### Deploying API
Docker sets up the server at ```http://localhost:8101```\
Change directory to docker-compose.yml location ```cd compose_api```\
Build Docker image ```docker compose build```\
Start the container ```docker compose up -d```
### Chunking
Endpoint ```/divide/```\
Request ```multipart/form-data``` ```file string($binary)``` ```chunk_size integer``` ```file_name string```\
Response ```StreamingResponse```
### Building
Endpoint ```/build/```\
Request ```multipart/form-data``` ```file string($binary)```\
Response ```StreamingResponse```

---
Swagger at ```/docs```
