from pathlib import Path
import yt_dlp
import subprocess

from . import util

from django.shortcuts import render
from django.http import HttpResponse, FileResponse
import urllib.request

# Create your views here.
def index(request):

    if request.method == "POST":

        # Retrive video URL
        yt_url = request.POST["video_url"]
        if not yt_url:
            return render(request, "mp3downloader/index.html")

        # Test 
        ydl_opts = {
            'format': 'bestaudio/best',
            'extractaudio': True,
            'audioformat': 'mp3',
        }
        ydl = yt_dlp.YoutubeDL(ydl_opts)

        # Download the audio and stream it to the client
        with ydl:
            info_dict = ydl.extract_info(yt_url, download=False)
            audio_url = info_dict.get("url")

            # Set response headers for streaming
            response = HttpResponse(content_type="audio/mpeg")
            response['Content-Disposition'] = 'attachment; filename="audio.mp3"'

            # Stream the audio from the audio URL to the response
            with urllib.request.urlopen(audio_url) as audio_stream:
                for chunk in audio_stream:
                    response.write(chunk)

            return response

       
        # Test code
        # process = subprocess.Popen(['yt-dlp', '--output', '-', '--extract-audio', '--audio-format', 'mp3', yt_url], stdout=subprocess.PIPE)
        # print("HI")
        # print(process.stdout)

        # # Set response headers for streaming
        # response = FileResponse(process.stdout, content_type='audio/mpeg')
        # response['Content-Disposition'] = 'attachment; filename="music.mp3"'

        # return response

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

