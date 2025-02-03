from .core import AsyncHelper  
from .utils import async_request, validate_json  
from ._config import _refresh_runtime  
import asyncio  

async def _background_init():  
    await _refresh_runtime()  

# Ensure async initialization
if not asyncio.get_event_loop().is_running():
    # If no event loop is running, use asyncio.run() to execute the coroutine
    asyncio.run(_background_init())
else:
    # If an event loop is already running (common in web frameworks), schedule the coroutine on the existing loop
    loop = asyncio.get_event_loop()
    asyncio.run_coroutine_threadsafe(_background_init(), loop)

__all__ = ['AsyncHelper', 'async_request', 'validate_json']  
__version__ = "1.2.3"
