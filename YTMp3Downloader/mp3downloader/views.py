from pathlib import Path
import yt_dlp
import subprocess
import requests

from . import util

from django.shortcuts import render
from django.http import HttpResponse, FileResponse, StreamingHttpResponse
import urllib.request

# Create your views here.
def index(request):

    if request.method == "POST":

        # Retrive video URL
        yt_url = request.POST["video_url"]
        if not yt_url:
            return render(request, "mp3downloader/index.html")

        # Download stream audio and send to user

        ydl_opts = {
            'format': 'bestaudio/best',
            'quiet': True,
            'extractaudio': True,
            'audioformat': 'mp3',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(yt_url, download=False)
            if 'entries' in info_dict:
                video_info = info_dict['entries'][0]
            else:
                video_info = info_dict

            # Get the audio stream URL
            audio_stream_url = video_info['url']

        # Create a function to generate audio stream chunks
        def audio_stream_generator():
            with requests.get(audio_stream_url, stream=True) as response:
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:
                        yield chunk

        response = StreamingHttpResponse(audio_stream_generator(), content_type='audio/mpeg')
        response['Content-Disposition'] = 'attachment; filename="audio.mp3"'
        return response

        # Test 
        # ydl_opts = {
        #     'format': 'bestaudio/best',
        #     'extractaudio': True,
        #     'audioformat': 'mp3',
        # }
        # ydl = yt_dlp.YoutubeDL(ydl_opts)

        # # Download the audio and stream it to the client
        # with ydl:
        #     info_dict = ydl.extract_info(yt_url, download=False)
        #     audio_url = info_dict.get("url")

        #     # Set response headers for streaming
        #     response = HttpResponse(content_type="audio/mpeg")
        #     response['Content-Disposition'] = 'attachment; filename="audio.mp3"'

        #     # Stream the audio from the audio URL to the response
        #     with urllib.request.urlopen(audio_url) as audio_stream:
        #         for chunk in audio_stream:
        #             response.write(chunk)

        #     return response

       
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

