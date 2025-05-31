import random
import ssl
import asyncio
from os.path import realpath

import aiohttp
from aiohttp import client_exceptions


class UnableToFetchCarbon(Exception):
    pass


themes = [
    "3024-night",
    "a11y-dark",
    "blackboard",
    "base16-dark",
    "base16-light",
    "cobalt",
    "duotone-dark",
    "dracula-pro",
    "hopscotch",
    "lucario",
    "material",
    "monokai",
    "nightowl",
    "nord",
    "oceanic-next",
    "one-light",
    "one-dark",
    "panda-syntax",
    "parasio-dark",
    "seti",
    "shades-of-purple",
    "solarized+dark",
    "solarized+light",
    "synthwave-84",
    "twilight",
    "verminal",
    "vscode",
    "yeti",
    "zenburn",
]

colour = [
    "#FF0000",
    "#FF5733",
    "#FFFF00",
    "#008000",
    "#0000FF",
    "#800080",
    "#A52A2A",
    "#FF00FF",
    "#D2B48C",
    "#00FFFF",
    "#808000",
    "#800000",
    "#00FFFF",
    "#30D5C8",
    "#00FF00",
    "#008080",
    "#4B0082",
    "#EE82EE",
    "#FFC0CB",
    "#000000",
    "#FFFFFF",
    "#808080",
]


class CarbonAPI:
    def __init__(self):
        self.language = "auto"
        self.drop_shadow = True
        self.drop_shadow_blur = "68px"
        self.drop_shadow_offset = "20px"
        self.font_family = "JetBrains Mono"
        self.width_adjustment = True
        self.watermark = False
        # Create SSL context for better connection handling
        self.ssl_context = ssl.create_default_context()
        self.ssl_context.check_hostname = False
        self.ssl_context.verify_mode = ssl.CERT_NONE

    async def generate(self, text: str, user_id):
        timeout = aiohttp.ClientTimeout(total=60, connect=15)
        connector = aiohttp.TCPConnector(
            limit=20,
            limit_per_host=5,
            ssl=self.ssl_context,
            force_close=True,
            enable_cleanup_closed=True
        )
        
        try:
            async with aiohttp.ClientSession(
                headers={"Content-Type": "application/json"},
                timeout=timeout,
                connector=connector
            ) as ses:
                params = {
                    "code": text,
                }
                params["backgroundColor"] = random.choice(colour)
                params["theme"] = random.choice(themes)
                params["dropShadow"] = self.drop_shadow
                params["dropShadowOffsetY"] = self.drop_shadow_offset
                params["dropShadowBlurRadius"] = self.drop_shadow_blur
                params["fontFamily"] = self.font_family
                params["language"] = self.language
                params["watermark"] = self.watermark
                params["widthAdjustment"] = self.width_adjustment
                
                try:
                    request = await ses.post(
                        "https://carbonara.solopov.dev/api/cook",
                        json=params,
                    )
                    if request.status != 200:
                        raise UnableToFetchCarbon(f"HTTP {request.status}")
                    resp = await request.read()
                    
                except (client_exceptions.ClientConnectorError, asyncio.TimeoutError, ssl.SSLError) as e:
                    print(f"Carbon API error: {e}")
                    raise UnableToFetchCarbon(f"Connection error: {e}")
                
                with open(f"cache/carbon{user_id}.jpg", "wb") as f:
                    f.write(resp)
                return realpath(f.name)
        except Exception as e:
            print(f"Carbon API generate error: {e}")
            raise UnableToFetchCarbon(f"Failed to generate carbon: {e}")
