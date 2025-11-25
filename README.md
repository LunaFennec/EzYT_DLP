# A simple, no fuss, no tech-savvy command line youtube video downloader using YT-DLP at it's core.

-------------------------------------------------------------------------------------------------------------
![icon](icon.ico)

### Usage:

* Download the latest release. Place the .exe wherever you like, and run it.

* Provide a video URL.
  > Only one URL at a time is supported.

* Choose quality by typing number 1-5.

* Choose filetype with number 1-2.

* Downloading will start and be placed in your regular downloads folder.

* The files will be output in the type and quality you selected.
  > If the quality is not available, the closest quality available will be chosen instead.

Check out all the [supported websites](supportedsites.md) you can download from.

---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Started off as a personal project to make downloading youtube videos easier. decided to publish it to github for others to use.

To build the source code, make sure to include ffmpeg, ffprobe and yt-dlp exe's as binaries. The icon is optional.

Simple one line to build:

``` pyinstaller --onefile --console --icon "icon.ico" --add-binary "yt-dlp.exe;." --add-binary "ffmpeg.exe;." --add-binary "ffprobe.exe;." download.py ```
