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

        # Test
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
        
        # ydl = yt_dlp.YoutubeDL()

        # # Set options for downloading and capturing output
        # options = {
        #     'format': 'bestaudio/best',
        #     'extractaudio': True,
        #     'audioformat': 'mp3',
        #     'outtmpl': "C:/Users/Rick/Documents/MyProject/YTMp3Downloader/YTMp3Downloader/file.mp3", # Output to stdout
        #     'quiet': False,  # Include status messages in output
        # }

        # with ydl:
        #     result = ydl.extract_info(yt_url, download=False, force_generic_extractor=True)
            
        #     audio_format = next((format for format in result['formats'] if format['ext'] in ['mp3', 'm4a', 'aac']), None)

        #     if audio_format:
        #         # Capture the output by running the download with the selected format's URL
        #         output = ydl.download([audio_format['url']])
        #     else:
        #         output = "No suitable audio format found for the video."


        # # The 'output' variable now contains the captured output
        # print(output)

        # return render(request, "mp3downloader/index.html", {
        #     'response': output
        # })

        # Test code
        # process = subprocess.Popen(['yt-dlp', '--output', '-', '--extract-audio', '--audio-format', 'mp3', yt_url], stdout=subprocess.PIPE)
        
        # print("HI")
        # while True:
        #     line = process.stdout.readline()
        #     if not line:
        #         break
        #     print(line, end='')


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

