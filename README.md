# A simple, no fuss, no tech-savvy command line youtube video downloader using YT-DLP at it's core for Windows.

-------------------------------------------------------------------------------------------------------------
![icon](icon.ico)

### Usage:

* Download the latest release. Place the .exe wherever you like, and run it. 

* Provide a video URL.
  > Only one URL at a time is supported.

* Hit enter.

* Downloading will start and be placed in your regular downloads folder.

* The files will be output as .mp4 with the highest available quality.
  > Take note, long high quality videos will take a long time to download and use up a lot of disk space!

Check out all the [supported websites](supportedsites.md) you can download from.

---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Started off as a personal project to make downloading youtube videos easier. decided to publish it to github for others to use.

To build the source code, make sure to include the icon.ico, ffmpeg, ffprobe and yt-dlp exe's. 

Simple one line to build:

``` pyinstaller --onefile --console --icon "icon.ico" --add-binary "yt-dlp.exe;." --add-binary "ffmpeg.exe;." --add-binary "ffprobe.exe;." download.py ```
