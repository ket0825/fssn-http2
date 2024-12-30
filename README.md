## HTTP/2 Simple Server With Python


### Description
- HTTP/2 Client: HTTPX Library
- HTTP/2 Server: Hypercorn Library with FASTAPI Framework

### Directories
- http2-client: HTTP/2 Client
- http2-server: HTTP/2 Simple Server
- http2-server-evolve: Add Exception Handling

### Installation
```python
poetry install
```

### Run Server
```python
poetry run hypercorn --certfile ./http2-server/cert.pem --keyfile ./http2-server/key.pem --bind localhost:8000 ./http2-server/server.py:app

or 

python ./http2-server-evolve/server.py
```

### Run Client
```bash
python ./http2-client/client.py --certfle ./http2-client/cert.pem --protocol http2
```

