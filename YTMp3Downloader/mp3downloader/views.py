from pathlib import Path
import yt_dlp
import subprocess

from . import util

from django.shortcuts import render
from django.http import HttpResponse

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

        # Use subprocess to call another yt-dlp program to download mp3
        # note change music to %(title)
        command = ['yt-dlp', '-f', 'ba', '-x', '--audio-format', 'mp3', yt_url, '-o', 'downloadmusic/music.%(ext)s']
        subprocess.call(command)
        
        # Get file which download on server and return it to user
        music_file = open('downloadmusic/music.mp3', 'rb')
        response = HttpResponse(music_file.read(), content_type='audio/mpeg')
        response['Content-Disposition'] = 'attachment; filename="music.mp3"'
        
        # Clean up download file
        music_file.close()
        subprocess.call(['rm', 'downloadmusic/music.mp3'])
    
        return response
        
        
        # # success
        # command = ['yt-dlp', yt_url, '--extract-audio', '--audio-format', 'mp3', '-o', 'downloaded_audio.%(ext)s']
        # subprocess.call(command)

        # # Serve the downloaded MP3 file as a response
        # audio_file = open('downloaded_audio.mp3', 'rb')
        # response = HttpResponse(audio_file.read(), content_type='audio/mpeg')
        # response['Content-Disposition'] = 'attachment; filename="downloaded_audio.mp3"'

        # # Clean up the downloaded files
        # audio_file.close()
        # subprocess.call(['rm', 'downloaded_audio.mp3'])

        # return response

        

    return render(request, "mp3downloader/index.html")

