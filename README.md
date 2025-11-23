A simple, no fuss, no tech-savvy command line youtube video downloader using YT-DLP at it's core for Windows.
-------------------------------------------------------------------------------------------------------------
![icon](icon.ico)

To use, simply download the latest release. Place the .exe wherever you like, and run it. 
You're prompted to provide a video URL(only 1 url at the time)
After hitting enter the program will simply download and then place the output file as a .mp4 in your regular downloads folder.
It will try to download at the highest quality available for that video, so take caution as long 4k videos can get big. I will add a quality setting soon.

Check out all the supported [websites](supportedsites.md).

---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Started off as a personal project to make downloading youtube videos easier. decided to publish it to github for others to use.

To build the source code, make sure to include the icon.ico, ffmpeg, ffprobe and yt-dlp exe's. 

Simple one line to build: pyinstaller --onefile --console --icon "myicon.ico" --add-binary "yt-dlp.exe;." --add-binary "ffmpeg.exe;." --add-binary "ffprobe.exe;." main.py
