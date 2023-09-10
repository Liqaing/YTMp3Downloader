# Youtube Mp3 Downloader

status: pause, pending

+ now
    - I think use javascript to download counld probably somehow work
    - send streaming audio url (rr2...) to frontend for javascript to download
    - but javascript could not download due to cross side origin error

    - i can use subprocess (with yt-dlp program) or yt-dlp module to download mp3 on server and send it to client with django httpresponse
    - however, when host on serverless web like vercel and railway, i could not install yt-dlp program for subprocess or download mp3 with yt-dlp module
    - on pythonanywhere which use virtual machine and server i could download yt-dlp program but becuase they restrict to api requests to some sites (includ youtube.com) for free tier account,  i can't make request. I could update my account and tride again.

    - i can use yt-dlp module to extract streaming audio url and other info, then use request module to get data from audio url, then send data to client without needing to download anything on server
    - however, it took too long and when in browser i counld not see how big the size of file is (it showed like this 3.4 mb / ?)
    - on vercel, when input the youtube video url and start download, it will terminate the request becuase it took too long (vercel allow like 5 sec for server to response or it cut off the request)
    - on railway, it took too long too, but it allowed me to download like 30% or so of the whole length, and then cut it off, so the mp3 only work like 30 second to 1 minute, and all that left is silence,
    - on pythonanywhere, same as above, it did not allow api request to youtube

i plan on build my own api for downloading mp3 from youtube, so without depending on other API for downloading mp3, i can download it with request to myserver
