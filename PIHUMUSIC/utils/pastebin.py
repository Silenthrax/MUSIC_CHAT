import aiohttp


import socket
from asyncio import get_running_loop
from functools import partial


def _netcat(host, port, content):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    s.sendall(content.encode())
    s.shutdown(socket.SHUT_WR)
    while True:
        data = s.recv(4096).decode("utf-8").strip("\n\x00")
        if not data:
            break
        return data
    s.close()


async def paste(content):
    loop = get_running_loop()
    link = await loop.run_in_executor(None, partial(_netcat, "ezup.dev", 9999, content))
    return link

####2nd paste code 

BASE = "https://batbin.me/"


async def post(url: str, *args, **kwargs):
    # Create SSL context for better connection handling
    import ssl
    import asyncio
    
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE
    
    timeout = aiohttp.ClientTimeout(total=30, connect=10)
    connector = aiohttp.TCPConnector(
        limit=20,
        limit_per_host=5,
        ssl=ssl_context,
        force_close=True,
        enable_cleanup_closed=True
    )
    
    try:
        async with aiohttp.ClientSession(
            timeout=timeout,
            connector=connector,
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        ) as session:
            async with session.post(url, *args, **kwargs) as resp:
                try:
                    data = await resp.json()
                except Exception:
                    data = await resp.text()
            return data
    except (aiohttp.ClientError, asyncio.TimeoutError, ssl.SSLError) as e:
        print(f"Pastebin API error: {e}")
        return None


async def PIHUBin(text):
    resp = await post(f"{BASE}api/v2/paste", data=text)
    if not resp or not resp.get("success"):
        return None
    link = BASE + resp["message"]
    return link
