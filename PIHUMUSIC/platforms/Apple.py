import re
import ssl
from typing import Union
import asyncio

import aiohttp
from bs4 import BeautifulSoup
from youtubesearchpython.__future__ import VideosSearch


class AppleAPI:
    def __init__(self):
        self.regex = r"^(https:\/\/music.apple.com\/)(.*)$"
        self.base = "https://music.apple.com/in/playlist/"
        # Create SSL context for better connection handling
        self.ssl_context = ssl.create_default_context()
        self.ssl_context.check_hostname = False
        self.ssl_context.verify_mode = ssl.CERT_NONE

    async def valid(self, link: str):
        if re.search(self.regex, link):
            return True
        else:
            return False

    async def track(self, url, playid: Union[bool, str] = None):
        if playid:
            url = self.base + url
        
        timeout = aiohttp.ClientTimeout(total=30, connect=10)
        connector = aiohttp.TCPConnector(
            limit=20,
            limit_per_host=5,
            ssl=self.ssl_context,
            force_close=True,
            enable_cleanup_closed=True
        )
        
        try:
            async with aiohttp.ClientSession(
                timeout=timeout,
                connector=connector,
                headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
            ) as session:
                async with session.get(url) as response:
                    if response.status != 200:
                        return False
                    html = await response.text()
        except (aiohttp.ClientError, asyncio.TimeoutError, ssl.SSLError) as e:
            print(f"Apple API track error: {e}")
            return False
        
        soup = BeautifulSoup(html, "html.parser")
        search = None
        for tag in soup.find_all("meta"):
            if tag.get("property", None) == "og:title":
                search = tag.get("content", None)
        if search is None:
            return False
        
        try:
            results = VideosSearch(search, limit=1)
            search_results = await results.next()
            if not search_results.get("result"):
                return False
                
            result = search_results["result"][0]
            title = result.get("title", "Unknown")
            ytlink = result.get("link", "")
            vidid = result.get("id", "")
            duration_min = result.get("duration", "0:00")
            thumbnails = result.get("thumbnails", [])
            thumbnail = thumbnails[0]["url"].split("?")[0] if thumbnails else ""
            
            track_details = {
                "title": title,
                "link": ytlink,
                "vidid": vidid,
                "duration_min": duration_min,
                "thumb": thumbnail,
            }
            return track_details, vidid
        except Exception as e:
            print(f"Apple API YouTube search error: {e}")
            return False

    async def playlist(self, url, playid: Union[bool, str] = None):
        if playid:
            url = self.base + url
        playlist_id = url.split("playlist/")[1]
        
        timeout = aiohttp.ClientTimeout(total=30, connect=10)
        connector = aiohttp.TCPConnector(
            limit=20,
            limit_per_host=5,
            ssl=self.ssl_context,
            force_close=True,
            enable_cleanup_closed=True
        )
        
        try:
            async with aiohttp.ClientSession(
                timeout=timeout,
                connector=connector,
                headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
            ) as session:
                async with session.get(url) as response:
                    if response.status != 200:
                        return False
                    html = await response.text()
        except (aiohttp.ClientError, asyncio.TimeoutError, ssl.SSLError) as e:
            print(f"Apple API playlist error: {e}")
            return False
        
        soup = BeautifulSoup(html, "html.parser")
        applelinks = soup.find_all("meta", attrs={"property": "music:song"})
        results = []
        for item in applelinks:
            try:
                content = item.get("content", "")
                if "album/" in content:
                    xx = content.split("album/")[1].split("/")[0].replace("-", " ")
                    results.append(xx)
            except Exception:
                continue
        return results, playlist_id
