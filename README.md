# A simple, no fuss, no tech-savvy youtube video downloader using YT-DLP at it's core.

--------------------------------------------------------------------------------------------------------------------
![icon](icon.ico)

### Usage:

* Install the program with the provided installer.

* Define video/audio settings. The default settings can be set in settings.

* Provide a video URL.
  > Only one URL at a time is supported. A queue system is in the works.

* Downloading will start and be placed in the selected download folder. It defaults to your native downloads folder.

* The files will be output in the type and quality you selected.
  > If the quality is not available, the closest quality available will be chosen instead.

Check out all the [supported websites](supportedsites.md) you can download from.

---------------------------------------------------------------------------------------------------------------------

Started off as a personal project to make downloading youtube videos easier. decided to publish it to github for others to use.

Build the app with:

```powershell
pyinstaller EZ_YT-DLP.spec
```

The app expects the bundled binaries `yt-dlp.exe`, `ffmpeg.exe`, and `ffprobe.exe` alongside the script or inside the packaged build.
