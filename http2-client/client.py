import httpx
import ssl
import argparse

async def main(config: argparse.Namespace):    
    ssl_context = ssl.create_default_context(cafile=config.certfile)
    protocol = {"http1": False, "http2": False}
    protocol[config.protocol] = True
    
    client = httpx.AsyncClient(
        verify=ssl_context,
        **protocol      
        )
    response = await client.get(config.address)
    print(response.text)
    await client.aclose()
    
if __name__ == "__main__":
    args = argparse.ArgumentParser()
    args.add_argument("--certfile", type=str, required=True) # "./http2-client/cert.pem"
    args.add_argument("--protocol", type=str, choices=["http1", "http2"], default="http2")
    args.add_argument("--address", type=str, default="https://localhost:8000/")
    args = args.parse_args()            
    
    import asyncio
    asyncio.run(main(args))
    
    