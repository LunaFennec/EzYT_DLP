import subprocess
import os
import shutil
from pathlib import Path
import sys
import re
import urllib.request

def get_exe_folder():
    # Safe access to _MEIPASS for PyInstaller single-file; fallback to script folder when running normally
    if getattr(sys, 'frozen', False):
        return Path(getattr(sys, "_MEIPASS", Path(__file__).parent))
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
        with urllib.request.urlopen(req, timeout=6):
            return True
    except:
        return False

def choose_quality():
    while True:
        prompt = (
            "Select quality (1-5):\n"
            " 1) 240p\n"
            " 2) 480p\n"
            " 3) 720p\n"
            " 4) 1080p\n"
            " 5) Max available (best)\n"
            "Choice: "
    )
    choice = input(prompt).strip()

    if choice in {"1","2","3","4","5"}:
        return choice
    
    print("Invalid choice. PPlease choose 1-5.")

def choose_mode():
    prompt = (
        "Download mode:\n"
        " 1) Video (mp4)\n"
        " 2) Audio only (m4a)\n"
        "Choice: "
    )
    choice = input(prompt).strip()

    if choice in {"1", "2"}:
        return choice
    
    print("Invalid choice. Press 1-2.")

def build_video_format(choice: str) -> str:
    mapping = {
        "1": "bestvideo[height<=240][ext=mp4]+bestaudio[ext=m4a]/best[height<=240][ext=mp4]/best",
        "2": "bestvideo[height<=480][ext=mp4]+bestaudio[ext=m4a]/best[height<=480][ext=mp4]/best",
        "3": "bestvideo[height<=720][ext=mp4]+bestaudio[ext=m4a]/best[height<=720][ext=mp4]/best",
        "4": "bestvideo[height<=1080][ext=mp4]+bestaudio[ext=m4a]/best[height<=1080][ext=mp4]/best",
        "5": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best"
    }
    return mapping.get(choice, mapping["5"])
    
    #Main loop

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
        print("It may be offline, blocked, or otherwise invalid.")
        input("\nPress Enter to exit...")
        return

    exe_folder = get_exe_folder()

    ytdlp_path = exe_folder / "yt-dlp.exe"
    ffmpeg_path = exe_folder / "ffmpeg.exe"
    ffprobe_path = exe_folder / "ffprobe.exe"

    os.environ["PATH"] = str(exe_folder) + os.pathsep + os.environ.get("PATH", "")

    downloads_folder = Path.home() / "Downloads"

    if not ytdlp_path.exists():
        print("yt-dlp.exe not found in the folder with this program. How did you manage this???")
        input("\nPress Enter to exit...")
        return

    # Ask quality and mode
    quality_choice = choose_quality()
    mode_choice = choose_mode()

    # Build yt-dlp args depending on mode
    if mode_choice == "1":
        # Video (mp4)
        fmt = build_video_format(quality_choice)
        ytdlp_args = [str(ytdlp_path), "-f", fmt, url]
        mode_text = f"Video (format: {fmt})"
    else:
        # Audio only -> extract to m4a using ffmpeg
        # Using -x will re-encode only if necessary; audio-quality 0 = best
        ytdlp_args = [str(ytdlp_path), "-x", "--audio-format", "m4a", "--audio-quality", "0", url]
        mode_text = "Audio only (m4a)"

    print(f"\nSelected: quality {quality_choice}, {mode_text}")
    print("\nDownloading…\n")

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
        print("yt-dlp reported an error:\n")
        print(result.stderr)
        input("\nPress Enter to exit...")
        return

    # Print yt-dlp stdout (download summary)
    print(result.stdout)

    print("\nMoving file(s) to Downloads…\n")

    # Allowed yt-dlp output file extensions (include expected audio/video containers)
    allowed_ext = {
        ".mp4", ".m4a", ".webm", ".mp3",
        ".info.json", ".description",
        ".jpg", ".jpeg", ".png", ".webp",
        ".vtt", ".srt"
    }

    moved_any = False

    for f in exe_folder.glob("*"):
        # Skip internal runtime files (PyInstaller temp files & executables)
        if f.name.lower().startswith(("yt-dlp", "ffmpeg", "ffprobe")):
            continue
        if f.suffix == ".exe":
            continue

        # Only move expected yt-dlp output files
        if f.suffix.lower() not in allowed_ext:
            continue

        if f.is_file():
            try:
                dest = downloads_folder / f.name
                # If file exists, avoid overwriting — add suffix
                if dest.exists():
                    base = dest.stem
                    ext = dest.suffix
                    count = 1
                    while True:
                        new_name = f"{base} ({count}){ext}"
                        new_dest = downloads_folder / new_name
                        if not new_dest.exists():
                            dest = new_dest
                            break
                        count += 1
                shutil.move(str(f), str(dest))
                print(f"Moved: {f.name} -> {dest.name}")
                moved_any = True
            except Exception as e:
                print(f"Unable to move {f.name}: {e}")

    if not moved_any:
        print("No output files were created.")
        print("This might mean the video is protected or otherwise unsupported.")

    print("\nDone.")
    input("Press Enter to exit...")
if __name__ == "__main__":
    main()

