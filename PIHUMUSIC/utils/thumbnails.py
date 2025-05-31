import os
import re
import ssl
import asyncio

import aiofiles
import aiohttp
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont
from unidecode import unidecode
from youtubesearchpython.__future__ import VideosSearch

from PIHUMUSIC import app
from config import YOUTUBE_IMG_URL
from PIHUMUSIC.utils.ssl_helper import create_safe_session


def changeImageSize(maxWidth, maxHeight, image):
    widthRatio = maxWidth / image.size[0]
    heightRatio = maxHeight / image.size[1]
    newWidth = int(widthRatio * image.size[0])
    newHeight = int(heightRatio * image.size[1])
    newImage = image.resize((newWidth, newHeight))
    return newImage


def clear(text):
    list = text.split(" ")
    title = ""
    for i in list:
        if len(title) + len(i) < 60:
            title += " " + i
    return title.strip()


async def get_thumb(videoid):
    if os.path.isfile(f"cache/{videoid}.png"):
        return f"cache/{videoid}.png"

    url = f"https://www.youtube.com/watch?v={videoid}"
    
    # Initialize default values
    title = "Unsupported Title"
    duration = "Unknown Mins"
    thumbnail = f"https://img.youtube.com/vi/{videoid}/hqdefault.jpg"
    views = "Unknown Views"
    channel = "Unknown Channel"
    
    try:
        results = VideosSearch(url, limit=1)
        for result in (await results.next())["result"]:
            try:
                title = result["title"]
                title = re.sub(r"\W+", " ", title)
                title = title.title()
            except:
                title = "Unsupported Title"
                
            try:
                duration = result["duration"]
            except:
                duration = "Unknown Mins"
                
            try:
                thumbnail = result["thumbnails"][0]["url"].split("?")[0]
            except:
                thumbnail = f"https://img.youtube.com/vi/{videoid}/hqdefault.jpg"
                
            try:
                views = result["viewCount"]["short"]
            except:
                views = "Unknown Views"
                
            try:
                channel = result["channel"]["name"]
            except:
                channel = "Unknown Channel"        # Download thumbnail using safe SSL session
        try:
            async with create_safe_session() as session:
                async with session.get(thumbnail) as resp:
                    if resp.status == 200:
                        async with aiofiles.open(f"cache/thumb{videoid}.png", mode="wb") as f:
                            await f.write(await resp.read())
        except Exception as e:
            print(f"Thumbnail download error: {e}")
            # Use default image if download fails
            return YOUTUBE_IMG_URL

        # Process the thumbnail image
        try:
            youtube = Image.open(f"cache/thumb{videoid}.png")
            image1 = changeImageSize(1280, 720, youtube)
            image2 = image1.convert("RGBA")
            background = image2.filter(filter=ImageFilter.BoxBlur(10))
            enhancer = ImageEnhance.Brightness(background)
            background = enhancer.enhance(0.5)
            draw = ImageDraw.Draw(background)
            
            arial = ImageFont.truetype("PIHUMUSIC/assets/font2.ttf", 30)
            font = ImageFont.truetype("PIHUMUSIC/assets/font.ttf", 30)
            
            # Use textbbox instead of deprecated textsize for newer Pillow versions
            try:
                text_bbox = draw.textbbox((0, 0), "TEAM KRITI BOTS    ", font=font)
                text_width = text_bbox[2] - text_bbox[0]
            except AttributeError:
                # Fallback for older Pillow versions
                text_size = draw.textsize("TEAM KRITI BOTS    ", font=font)
                text_width = text_size[0]
            
            draw.text((1280 - text_width - 10, 10), "TEAM KRITI BOTS    ", fill="white", font=font)
            draw.text(
                (55, 560),
                f"{channel} | {views[:23]}",
                (255, 255, 255),
                font=arial,
            )
            draw.text(
                (57, 600),
                clear(title),
                (255, 255, 255),
                font=font,
            )
            draw.line(
                [(55, 660), (1220, 660)],
                fill="white",
                width=5,
                joint="curve",
            )
            draw.ellipse(
                [(918, 648), (942, 672)],
                outline="white",
                fill="white",
                width=15,
            )
            draw.text(
                (36, 685),
                "00:00",
                (255, 255, 255),
                font=arial,
            )
            draw.text(
                (1185, 685),
                f"{duration[:23]}",
                (255, 255, 255),
                font=arial,
            )
            
            # Clean up temporary file
            try:
                os.remove(f"cache/thumb{videoid}.png")
            except:
                pass
                
            background.save(f"cache/{videoid}.png")
            return f"cache/{videoid}.png"
            
        except Exception as e:
            print(f"Image processing error: {e}")
            return YOUTUBE_IMG_URL
            
    except Exception as e:
        print(f"Thumbnail generation error: {e}")
        return YOUTUBE_IMG_URL
