A simple, no fuss, no tech-savvy python-based youtube video downloader using YT-DLP at it's core for Windows.
-------------------------------------------------------------------------------------------------------------
Built using PyInstaller.
To build the source code, make sure to include the icon.ico, ffmpeg, ffprobe and yt-dlp exe's. 

Simple one line to build: pyinstaller --onefile --console --icon "myicon.ico" --add-binary "yt-dlp.exe;." --add-binary "ffmpeg.exe;." --add-binary "ffprobe.exe;." main.py
