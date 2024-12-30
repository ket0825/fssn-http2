from fastapi import FastAPI
from fastapi.requests import Request
from fastapi.responses import HTMLResponse

app = FastAPI()

def check_tls(certfile: str, keyfile: str) -> bool:
    import os
    if not os.path.exists(certfile) and not str(certfile).endswith(".pem"):
        print(f"Certificate file {certfile} not found")
        return False
    if not os.path.exists(keyfile) and not str(keyfile).endswith(".pem"):
        print(f"Key file {keyfile} not found")
        return False
    return True

@app.get("/")
async def read_root(request: Request) -> HTMLResponse:
    client_host = request.client.host
    client_port = request.client.port
    client_addr = f"{client_host}:{client_port}"
    protocol = request.headers.get("X-Forwarded-Proto", "http")    
    http_version = request.scope.get("http_version")
    print(f"Got connection: {protocol}/{http_version} from {client_addr}")
    return HTMLResponse(content=f"Hello")

if __name__ == "__main__":
    import hypercorn
    import hypercorn.asyncio
    config = hypercorn.Config()
    config.bind = ["localhost:443", "localhost:80"]    
    
    config.certfile = "./http2-server/cert.pem"
    config.keyfile = "./http2-server/key.pem"    
    config.alpn_protocols = ["h2", "http/1.1"]
    
    if config.ssl_enabled:
        print(f"Running on https://localhost:443 (CTRL + C to quit)")
    else:
        print(f"Running on http://localhost:80 (CTRL + C to quit)")                        

    if "h2" in config.alpn_protocols:
        print("HTTP/2 is enabled")
    elif "http/1.1" in config.alpn_protocols:
        print("HTTP/1.1 is enabled")
    else:
        print("HTTP/2 and HTTP/1.1 are disabled")
        
    if not check_tls(config.certfile, config.keyfile):
        raise("TLS configuration error")        
    
    import asyncio
    asyncio.run(hypercorn.asyncio.serve(app, config))

# MARK: CMD below
# poetry run hypercorn --certfile ./http2-server/cert.pem --keyfile ./http2-server/key.pem --bind localhost:8000 ./http2-server-evolve/server.py:app