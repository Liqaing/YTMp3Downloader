from pathlib import Path
import yt_dlp
import json
import subprocess
import requests

from . import util

from django.shortcuts import render
from django.http import HttpResponse, FileResponse, StreamingHttpResponse
import urllib.request

from django.views.decorators.csrf import csrf_exempt

# Create your views here.
@csrf_exempt
def index(request):

    if request.method == "POST":

        # Retrive video URL
        yt_url = request.POST["video_url"]
        if not yt_url:
            return render(request, "mp3downloader/index.html")

        # Test, retrun stream audio url
        ydl_opts = {
            # Ba = Best audio format
            'format': 'ba',
            'extract-audio': True,
            'audio-format': 'mp3'
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(yt_url, download=False)
            mp3_audio_url = info['url']
        return render(request, "mp3downloader/index.html", {
            # 'response': json.dumps(ydl.sanitize_info(info))
            'response': mp3_audio_url
        })

        # My code
        # # Retrive video id
        # yt_video_id = util.get_yt_video_id(yt_url)
        # if not yt_video_id:
        #     return render(request, "mp3downloader/index.html")

        # # Use subprocess to call another yt-dlp program to download mp3
        # # note change music to %(title)
        # command = ['yt-dlp', '-f', 'ba', '-x', '--audio-format', 'mp3', yt_url, '-o', 'downloadmusic/music.%(ext)s']
        # subprocess.call(command)
        
        # # Get file which download on server and return it to user
        # music_file = open('downloadmusic/music.mp3', 'rb')
        # response = HttpResponse(music_file.read(), content_type='audio/mpeg')
        # response['Content-Disposition'] = 'attachment; filename="music.mp3"'
        
        # # Clean up download file
        # music_file.close()
        # subprocess.call(['rm', 'downloadmusic/music.mp3'])
    
        # return response

    return render(request, "mp3downloader/index.html")

