import subprocess
import os
import shutil
from pathlib import Path
import sys
import re
import urllib.request


def get_exe_folder():
    if getattr(sys, 'frozen', False):
        return Path(sys._MEIPASS)
    else:
        return Path(__file__).parent


def is_valid_url(url: str) -> bool:
    url_regex = re.compile(
        r'^(https?://)'
        r'([\w.-]+)'
        r'(:\d+)?'
        r'(\/.*)?$',
        re.IGNORECASE
    )
    return re.match(url_regex, url) is not None


def check_url_exists(url: str) -> bool:
    try:
        req = urllib.request.Request(url, method="HEAD")
        with urllib.request.urlopen(req, timeout=5):
            return True
    except:
        return False


def main():
    os.system("title Easy YT_DLP Downloader")

    url = input("Video URL: ").strip()

    if not url:
        print("No URL detected.")
        input("\nPress Enter to exit...")
        return
    if not is_valid_url(url):
        print("Error: Invalid URL.")
        print("Make sure it begins with http:// or https:// and is supported.")
        input("\nPress Enter to exit...")
        return

    print("Checking URL…")
    if not check_url_exists(url):
        print("Cannot reach this URL.")
        print("It may be offline, blocked, or invalid.")
        input("\nPress Enter to exit...")
        return

    exe_folder = get_exe_folder()

    ytdlp_path = exe_folder / "yt-dlp.exe"
    ffmpeg_path = exe_folder / "ffmpeg.exe"
    ffprobe_path = exe_folder / "ffprobe.exe"

    os.environ["PATH"] = str(exe_folder) + os.pathsep + os.environ["PATH"]

    downloads_folder = Path.home() / "Downloads"

    if not ytdlp_path.exists():
        print("yt-dlp.exe not found. How did you manage to do this?? It's baked together!")
        input("\nPress Enter to exit...")
        return

    print("\nDownloading…\n")

    ytdlp_args = [
        str(ytdlp_path),
        "-f", "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
        url
    ]

    try:
        result = subprocess.run(
            ytdlp_args,
            cwd=exe_folder,
            text=True,
            capture_output=True
        )
    except Exception as e:
        print("yt-dlp failed to run.")
        print("Error:", e)
        input("\nPress Enter to exit...")
        return

    if result.returncode != 0:
        print("yt-dlp caused an error.\n")
        print(result.stderr)
        input("\nPress Enter to exit...")
        return

    print(result.stdout)
    print("\nMoving file to Downloads…\n")

    allowed_ext = {
        ".mp4", ".m4a", ".webm", ".mp3",
        ".info.json", ".description",
        ".jpg", ".jpeg", ".png", ".webp",
        ".vtt", ".srt"
    }

    moved_any = False

    for f in exe_folder.glob("*"):
        if f.name.lower().startswith(("yt-dlp", "ffmpeg", "ffprobe")):
            continue
        if f.suffix == ".exe":
            continue
        if f.suffix.lower() not in allowed_ext:
            continue

        if f.is_file():
            try:
                shutil.move(str(f), str(downloads_folder / f.name))
                print(f"Moved: {f.name}")
                moved_any = True
            except Exception as e:
                print(f"Unable to move {f.name}: {e}")

    if not moved_any:
        print("No output files were created.")
        print("This might mean the video is protected or somehow unsupported.")

    print("\nDone.")
    input("Press Enter to exit...")


if __name__ == "__main__":
    main()