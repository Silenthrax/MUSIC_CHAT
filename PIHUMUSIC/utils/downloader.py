from os import path
import yt_dlp
from yt_dlp.utils import DownloadError

ytdl = yt_dlp.YoutubeDL(
    {
        "outtmpl": "downloads/%(id)s.%(ext)s",
        "format": "bestaudio[ext=m4a]",
        "geo_bypass": True,
        "nocheckcertificate": True,
    }
 )


def download(url: str, my_hook) -> str:       
    ydl_optssx = {
        'format' : 'bestaudio[ext=m4a]',
        "outtmpl": "downloads/%(id)s.%(ext)s",
        "geo_bypass": True,
        "nocheckcertificate": True,
        'quiet': True,
        'no_warnings': True,
    }
    try:
        info = ytdl.extract_info(url, False)
        x = yt_dlp.YoutubeDL(ydl_optssx)
        x.add_progress_hook(my_hook)
        x.download([url])
        xyz = path.join("downloads", f"{info['id']}.{info['ext']}")
        return xyz
    except Exception as y_e:
        print(f"Download error: {y_e}")
        return None
