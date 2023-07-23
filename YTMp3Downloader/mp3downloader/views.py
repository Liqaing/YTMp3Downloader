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
            # Cannot retrive the video id
            return render(request, "mp3downloader/index.html")

        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }]
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([yt_video_id])

        return render(request, "mp3downloader/index.html")

    return render(request, "mp3downloader/index.html")

