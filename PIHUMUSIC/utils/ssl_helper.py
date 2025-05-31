import ssl
import asyncio
import aiohttp
import logging

# Configure logging for SSL errors
logger = logging.getLogger(__name__)

def create_ssl_context():
    """Create a permissive SSL context for better connection handling."""
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE
    return ssl_context

def create_connector():
    """Create an aiohttp connector with optimized settings."""
    return aiohttp.TCPConnector(
        limit=20,
        limit_per_host=5,
        ssl=create_ssl_context(),
        force_close=True,
        enable_cleanup_closed=True,
        keepalive_timeout=30
    )

async def safe_http_request(session, method, url, **kwargs):
    """Make a safe HTTP request with proper error handling."""
    try:
        async with session.request(method, url, **kwargs) as response:
            return response
    except (aiohttp.ClientError, asyncio.TimeoutError, ssl.SSLError) as e:
        logger.error(f"HTTP request failed for {url}: {e}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error in HTTP request for {url}: {e}")
        return None

def create_safe_session():
    """Create a safe aiohttp session with proper SSL handling."""
    timeout = aiohttp.ClientTimeout(total=30, connect=10)
    connector = aiohttp.TCPConnector(
        limit=20,
        limit_per_host=5,
        ssl=create_ssl_context(),
        force_close=True,
        enable_cleanup_closed=True
    )
    
    return aiohttp.ClientSession(
        timeout=timeout,
        connector=connector,
        headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    )

def handle_future_exception(future):
    """Handle exceptions from asyncio futures."""
    try:
        future.result()
    except Exception as e:
        logger.error(f"Future exception: {e}")

def handle_async_exception(loop, context):
    """Handle exceptions from asyncio event loop."""
    exception = context.get('exception')
    if exception:
        logger.error(f"Asyncio exception: {exception}")

def set_exception_handler():
    """Set a custom exception handler for the asyncio event loop."""
    def exception_handler(loop, context):
        exception = context.get('exception')
        if exception:
            logger.error(f"Asyncio exception: {exception}")
    
    loop = asyncio.get_event_loop()
    loop.set_exception_handler(exception_handler)
