from pathlib import Path
import yt_dlp

from . import util

from django.shortcuts import render

# Create your views here.
def index(request):

    if request.method == "POST":

        # Retrive video URL
        yt_url = request.POST["video_url"]
        if not yt_url:
            return render(request, "mp3downloader/index.html")
        
        # Retrive video id
        yt_video_id = util.get_yt_video_id(yt_url)
        if not yt_video_id:
            return render(request, "mp3downloader/index.html")

        # Download video as mp3
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            # 'outtmpl': r'C:\Users\Rick\Downloads',
        }
        
        ydl = yt_dlp.YoutubeDL(ydl_opts)
        info_dict = ydl.extract_info(yt_video_id, download=True)

        print(info_dict)

        return render(request, "mp3downloader/index.html")

    return render(request, "mp3downloader/index.html")

