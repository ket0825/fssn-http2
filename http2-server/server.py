from fastapi import FastAPI
from fastapi.requests import Request
from fastapi.responses import HTMLResponse
import hypercorn.asyncio

app = FastAPI()

@app.get("/")
async def read_root(request: Request):
    client_host = request.client.host
    client_port = request.client.port
    client_addr = f"{client_host}:{client_port}"
    protocol = request.headers.get("X-Forwarded-Proto", "http")    
    http_version = request.scope.get("http_version")
    print(f"Got connection: {protocol}/{http_version} from {client_addr}")
    return HTMLResponse(content=f"Hello")

# if __name__ == "__main__":
#     import hypercorn
#     config = hypercorn.Config()
#     config.bind = ["localhost:443", "localhost:80"]    
    
#     config.certfile = "./http2-server/cert.pem"
#     config.keyfile = "./http2-server/key.pem"    
    
#     import asyncio
#     asyncio.run(hypercorn.asyncio.serve(app, config))

# MARK: CMD below
# poetry run hypercorn --certfile ./http2-server/cert.pem --keyfile ./http2-server/key.pem --bind localhost:8000 ./http2-server/server.py:app