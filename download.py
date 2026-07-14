import html
import json
import os
import re
import shutil
import subprocess
import sys
import time
import urllib.error
import urllib.request
import webbrowser
from pathlib import Path

from PySide6.QtCore import Qt, QThread, Signal, QTimer, QRect
from PySide6.QtGui import QIcon, QFont, QColor, QPalette, QTextCursor, QPainter
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QLabel,
    QLineEdit,
    QComboBox,
    QPushButton,
    QTextEdit,
    QFileDialog,
    QMessageBox,
    QCheckBox,
    QStackedWidget,
    QFrame,
    QButtonGroup,
)

APP_VERSION = "1.4.0"
YTDLP_RELEASE_API_URL = "https://api.github.com/repos/yt-dlp/yt-dlp/releases/latest"
APP_RELEASE_API_URL = "https://api.github.com/repos/LunaFennec/EzYT_DLP/releases/latest"
APP_RELEASE_URL = "https://github.com/LunaFennec/EzYT_DLP/releases"
CONFIG_FILE_NAME = "ezyt-dlp-config.json"

# ---------------------------------------------------------------------------
# Theme
# ---------------------------------------------------------------------------
BG_MAIN = "#3B3A3C"       
BG_SIDEBAR = "#2A292B"    
BG_PANEL = "#323133"      
BG_INPUT = "#4A484B"      
BG_CONSOLE = "#232224"    
BORDER = "#232224"
ACCENT = "#B40C04"        
ACCENT_HOVER = "#D10E05"
ACCENT_PRESSED = "#8E0A03"
TEXT_PRIMARY = "#FFFFFF"
TEXT_SECONDARY = "#B3B0B2"
TEXT_MUTED = "#8A8789"

STYLESHEET = f"""
* {{
    font-family: "Segoe UI", "Helvetica Neue", Arial, sans-serif;
}}

QMainWindow {{
    background-color: {BG_MAIN};
}}

#Sidebar {{
    background-color: {BG_SIDEBAR};
    border-right: 1px solid {BORDER};
}}

#SidebarTitle {{
    color: {TEXT_PRIMARY};
    font-size: 17px;
    font-weight: 700;
    padding: 4px 2px 2px 2px;
}}

#SidebarSubtitle {{
    color: {TEXT_MUTED};
    font-size: 11px;
    padding-bottom: 8px;
}}

QPushButton#NavButton {{
    text-align: left;
    color: {TEXT_SECONDARY};
    background-color: transparent;
    border: none;
    border-left: 3px solid transparent;
    padding: 10px 14px;
    font-size: 13px;
    font-weight: 600;
    border-radius: 0px;
}}

QPushButton#NavButton:hover {{
    color: {TEXT_PRIMARY};
    background-color: #343335;
}}

QPushButton#NavButton:checked {{
    color: {TEXT_PRIMARY};
    background-color: #343335;
    border-left: 3px solid {ACCENT};
}}

#PageTitle {{
    color: {TEXT_PRIMARY};
    font-size: 22px;
    font-weight: 700;
}}

#SectionLabel {{
    color: {TEXT_SECONDARY};
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 0.5px;
    text-transform: uppercase;
}}

QLineEdit {{
    background-color: {BG_INPUT};
    color: {TEXT_PRIMARY};
    border: 1px solid #59575A;
    border-radius: 6px;
    padding: 8px 10px;
    font-size: 13px;
    selection-background-color: {ACCENT};
}}

QLineEdit:focus {{
    border: 1px solid {ACCENT};
}}

QComboBox {{
    background-color: {BG_INPUT};
    color: {TEXT_PRIMARY};
    border: 1px solid #59575A;
    border-radius: 6px;
    padding: 7px 10px;
    font-size: 13px;
    min-width: 110px;
}}

QComboBox:hover {{
    border: 1px solid #7A787B;
}}

QComboBox::drop-down {{
    border: none;
    width: 24px;
}}

QComboBox QAbstractItemView {{
    background-color: {BG_PANEL};
    color: {TEXT_PRIMARY};
    border: 1px solid {BORDER};
    selection-background-color: {ACCENT};
    selection-color: {TEXT_PRIMARY};
    outline: none;
    padding: 4px;
}}

QPushButton#PrimaryButton {{
    background-color: {ACCENT};
    color: {TEXT_PRIMARY};
    border: none;
    border-radius: 20px;
    padding: 11px 34px;
    font-size: 13px;
    font-weight: 700;
    letter-spacing: 0.5px;
}}

QPushButton#PrimaryButton:hover {{
    background-color: {ACCENT_HOVER};
}}

QPushButton#PrimaryButton:pressed {{
    background-color: {ACCENT_PRESSED};
}}

QPushButton#PrimaryButton:disabled {{
    background-color: #5A585B;
    color: {TEXT_MUTED};
}}

QPushButton#SecondaryButton {{
    background-color: transparent;
    color: {TEXT_PRIMARY};
    border: 1px solid #6E6C6F;
    border-radius: 16px;
    padding: 8px 20px;
    font-size: 12px;
    font-weight: 600;
}}

QPushButton#SecondaryButton:hover {{
    border: 1px solid {TEXT_PRIMARY};
}}

QPushButton#GhostButton {{
    background-color: transparent;
    color: {TEXT_SECONDARY};
    border: none;
    padding: 6px 8px;
    font-size: 12px;
    font-weight: 600;
    text-decoration: underline;
}}

QPushButton#GhostButton:hover {{
    color: {TEXT_PRIMARY};
}}

#ConsoleFrame {{
    background-color: {BG_CONSOLE};
    border: 1px solid {BORDER};
    border-radius: 8px;
}}

#ConsoleHeader {{
    background-color: #1D1C1D;
    border-top-left-radius: 8px;
    border-top-right-radius: 8px;
    border-bottom: 1px solid {BORDER};
}}

#ConsoleTitle {{
    color: {TEXT_SECONDARY};
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 1px;
}}

#ConsoleStatus {{
    font-size: 11px;
    font-weight: 600;
}}

QTextEdit#Console {{
    background-color: transparent;
    color: {TEXT_SECONDARY};
    border: none;
    padding: 10px;
    font-family: Consolas, "Courier New", monospace;
    font-size: 12px;
}}

QCheckBox {{
    color: {TEXT_SECONDARY};
    font-size: 12px;
    spacing: 8px;
}}

QCheckBox::indicator {{
    width: 16px;
    height: 16px;
    border: 1px solid #7A787B;
    border-radius: 3px;
    background-color: {BG_INPUT};
    padding: 0px;
}}

QCheckBox::indicator:unchecked {{
    background-color: {BG_INPUT};
}}

QCheckBox::indicator:checked {{
    background-color: {BG_PANEL};
    border: 1px solid {ACCENT};
}}

QCheckBox::indicator:checked:hover {{
    background-color: {BG_MAIN};
    border: 1px solid {ACCENT_HOVER};
}}

QScrollBar:vertical {{
    background: transparent;
    width: 10px;
    margin: 2px;
}}

QScrollBar::handle:vertical {{
    background: #5A585C;
    border-radius: 5px;
    min-height: 24px;
}}

QScrollBar::handle:vertical:hover {{
    background: {ACCENT};
}}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
    height: 0px;
}}

QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {{
    background: transparent;
}}

QMessageBox {{
    background-color: {BG_MAIN};
}}
"""

def get_exe_folder() -> Path:
    if getattr(sys, "frozen", False):
        return Path(getattr(sys, "_MEIPASS", Path(__file__).parent))
    return Path(__file__).parent


def get_app_icon_path() -> Path:
    for base_dir in (get_exe_folder(), Path(__file__).parent):
        icon_path = base_dir / "icon.ico"
        if icon_path.exists():
            return icon_path
    return Path(__file__).parent / "icon.ico"


def is_valid_url(url: str) -> bool:
    pattern = re.compile(r"^(https?://)([\w.-]+)(:\d+)?(/.*)?$", re.IGNORECASE)
    return re.match(pattern, url) is not None


def compare_versions(left: str, right: str) -> int:
    left_parts = [int(part) for part in re.findall(r"\d+", left.lstrip("v"))]
    right_parts = [int(part) for part in re.findall(r"\d+", right.lstrip("v"))]
    max_len = max(len(left_parts), len(right_parts))
    left_parts.extend([0] * (max_len - len(left_parts)))
    right_parts.extend([0] * (max_len - len(right_parts)))
    if left_parts < right_parts:
        return -1
    if left_parts > right_parts:
        return 1
    return 0


def fetch_json(url: str):
    request = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(request, timeout=20) as response:
        return json.loads(response.read().decode("utf-8"))


def download_file(url: str, destination: Path) -> bool:
    try:
        request = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(request, timeout=60) as response, open(destination, "wb") as handle:
            shutil.copyfileobj(response, handle)
        return destination.exists() and destination.stat().st_size > 0
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, OSError):
        return False


def get_ytdlp_version(exe_path: Path):
    try:
        proc = subprocess.run(
            [str(exe_path), "--version"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=20,
        )
        if proc.returncode != 0:
            return None
        version = proc.stdout.strip().splitlines()[0].strip()
        if version.startswith("yt-dlp "):
            return version.replace("yt-dlp ", "", 1)
        return version
    except Exception:
        return None


def update_ytdlp_binary(ytdlp_path: Path):
    try:
        release = fetch_json(YTDLP_RELEASE_API_URL)
    except Exception:
        return False, "failed_to_check"

    latest_version = str(release.get("tag_name", "")).lstrip("v")
    if not latest_version:
        return False, "failed_to_check"

    local_version = get_ytdlp_version(ytdlp_path)
    if local_version and compare_versions(latest_version, local_version) <= 0:
        return False, "up_to_date"

    download_url = "https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp.exe"
    temp_path = ytdlp_path.with_suffix(".exe.tmp")
    try:
        if not download_file(download_url, temp_path):
            return False, "update_failed"
        if ytdlp_path.exists():
            ytdlp_path.unlink()
        os.replace(temp_path, ytdlp_path)
        return True, "updated"
    finally:
        if temp_path.exists():
            temp_path.unlink(missing_ok=True)


def build_video_format(choice: str) -> str:
    mapping = {
        "1": "bestvideo[height<=240][ext=mp4]+bestaudio[ext=m4a]/best[height<=240][ext=mp4]/best",
        "2": "bestvideo[height<=480][ext=mp4]+bestaudio[ext=m4a]/best[height<=480][ext=mp4]/best",
        "3": "bestvideo[height<=720][ext=mp4]+bestaudio[ext=m4a]/best[height<=720][ext=mp4]/best",
        "4": "bestvideo[height<=1080][ext=mp4]+bestaudio[ext=m4a]/best[height<=1080][ext=mp4]/best",
        "5": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
    }
    return mapping.get(choice, mapping["5"])


def build_audio_args(ytdlp_path: Path, url: str, bitrate: str) -> list:
    return [
        str(ytdlp_path),
        "-x",
        "--audio-format",
        "mp3",
        "--audio-quality",
        "2",
        "--postprocessor-args",
        f"ffmpeg:-b:a {bitrate} -ar 44100",
        url,
    ]


def get_config_path() -> Path:
    appdata = os.environ.get("APPDATA")
    if appdata:
        return Path(appdata) / "EZ_YT-DLP" / CONFIG_FILE_NAME
    return Path.home() / ".ezyt-dlp" / CONFIG_FILE_NAME


def load_config() -> dict:
    config_path = get_config_path()
    if not config_path.exists():
        return {}
    try:
        with open(config_path, "r", encoding="utf-8") as handle:
            data = json.load(handle)
            if isinstance(data, dict):
                return data
    except Exception:
        pass
    return {}


def save_config(config: dict) -> None:
    config_path = get_config_path()
    try:
        config_path.parent.mkdir(parents=True, exist_ok=True)
        with open(config_path, "w", encoding="utf-8") as handle:
            json.dump(config, handle, indent=2)
    except Exception:
        pass


ALLOWED_OUTPUT_EXT = {
    ".mp4", ".m4a", ".webm", ".mp3", ".info.json",
    ".description", ".jpg", ".jpeg", ".png", ".webp", ".vtt", ".srt",
}


class UpdateCheckThread(QThread):
    log = Signal(str)
    app_update_found = Signal(str, str)

    def __init__(self, ytdlp_path: Path, skip_app_prompt: bool):
        super().__init__()
        self.ytdlp_path = ytdlp_path
        self.skip_app_prompt = skip_app_prompt

    def run(self) -> None:
        if not self.ytdlp_path.exists():
            self.log.emit("yt-dlp.exe not found next to the program.")
        else:
            self.log.emit("Checking for yt-dlp updates...")
            try:
                _, status = update_ytdlp_binary(self.ytdlp_path)
            except Exception:
                status = "failed_to_check"

            if status == "updated":
                self.log.emit("yt-dlp updated successfully!")
            elif status == "up_to_date":
                self.log.emit("yt-dlp is up to date!")
            elif status == "update_failed":
                self.log.emit("yt-dlp update failed. Using older version.")
            else:
                self.log.emit("yt-dlp update check could not be completed.")

        if not getattr(sys, "frozen", False):
            return
        if self.skip_app_prompt:
            self.log.emit("Program update prompt skipped.")
            return
        try:
            release = fetch_json(APP_RELEASE_API_URL)
        except Exception:
            return

        latest_tag = str(release.get("tag_name", "")).lstrip("v")
        if not latest_tag:
            return
        if compare_versions(latest_tag, APP_VERSION) <= 0:
            return

        release_url = release.get("html_url") or APP_RELEASE_URL
        self.app_update_found.emit(latest_tag, release_url)


class DownloadThread(QThread):
    log = Signal(str)
    finished_download = Signal()

    def __init__(self, ytdlp_path: Path, exe_folder: Path, downloads_folder: Path,
                 url: str, mode: str, quality: str, bitrate: str):
        super().__init__()
        self.ytdlp_path = ytdlp_path
        self.exe_folder = exe_folder
        self.downloads_folder = downloads_folder
        self.url = url
        self.mode = mode
        self.quality = quality
        self.bitrate = bitrate

    def run(self) -> None:
        os.environ["PATH"] = str(self.exe_folder) + os.pathsep + (os.environ.get("PATH") or "")

        try:
            self.log.emit("Updating yt-dlp if needed...")
            _, status = update_ytdlp_binary(self.ytdlp_path)
            if status == "updated":
                self.log.emit("yt-dlp updated successfully.")
            elif status == "up_to_date":
                self.log.emit("yt-dlp is already up to date.")
            elif status == "update_failed":
                self.log.emit("yt-dlp update failed. The existing copy will be used.")
            else:
                self.log.emit("yt-dlp update check could not be completed.")
        except Exception as exc:
            self.log.emit(f"yt-dlp update check failed: {exc}")

        if self.mode == "Audio only":
            ytdlp_args = build_audio_args(self.ytdlp_path, self.url, self.bitrate)
            mode_text = f"Audio only (mp3, {self.bitrate})"
        else:
            quality_map = {"240p": "1", "480p": "2", "720p": "3", "1080p": "4", "Best": "5"}
            fmt = build_video_format(quality_map.get(self.quality, "5"))
            ytdlp_args = [str(self.ytdlp_path), "-f", fmt, self.url]
            mode_text = f"Video ({self.quality})"

        self.log.emit(f"Selected: {mode_text}")
        self.log.emit("Downloading...")

        try:
            process = subprocess.Popen(
                ytdlp_args,
                cwd=self.exe_folder,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
            )
            if process.stdout is not None:
                for line in iter(process.stdout.readline, ""):
                    if line:
                        self.log.emit(line.rstrip())
            else:
                self.log.emit("Unable to capture yt-dlp output.")
            return_code = process.wait()
        except Exception as exc:
            self.log.emit(f"yt-dlp failed: {exc}")
            self.finished_download.emit()
            return

        if return_code != 0:
            self.log.emit("Download finished with errors.")
            self.finished_download.emit()
            return

        self.downloads_folder.mkdir(parents=True, exist_ok=True)
        self.log.emit(f"Moving output files to {self.downloads_folder}...")
        self._move_downloaded_files()
        self.finished_download.emit()

    def _move_downloaded_files(self) -> None:
        moved_any = False
        for file_path in self.exe_folder.glob("*"):
            if file_path.name.lower().startswith(("yt-dlp", "ffmpeg", "ffprobe")):
                continue
            if file_path.suffix == ".exe":
                continue
            if file_path.suffix.lower() not in ALLOWED_OUTPUT_EXT:
                continue
            if not file_path.is_file():
                continue

            try:
                dest = self.downloads_folder / file_path.name
                if dest.exists():
                    base = dest.stem
                    ext = dest.suffix
                    count = 1
                    while True:
                        new_dest = self.downloads_folder / f"{base} ({count}){ext}"
                        if not new_dest.exists():
                            dest = new_dest
                            break
                        count += 1
                shutil.move(str(file_path), str(dest))
                moved_any = True
            except Exception as exc:
                self.log.emit(f"Unable to move {file_path.name}: {exc}")

        if moved_any:
            self.log.emit(f"Finished moving files to {self.downloads_folder}.")
        else:
            self.log.emit("No output files were created.")


class ToggleSwitch(QCheckBox):
    def __init__(self, text: str = "", parent=None) -> None:
        super().__init__(text, parent)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

    def paintEvent(self, event) -> None:
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        track_rect = QRect(0, (self.height() - 20) // 2, 44, 20)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QColor(ACCENT if self.isChecked() else BG_INPUT))
        painter.drawRoundedRect(track_rect, 10, 10)

        knob_size = 14
        knob_y = track_rect.center().y() - knob_size // 2
        knob_x = track_rect.left() + 3 if not self.isChecked() else track_rect.right() - knob_size - 3
        knob_rect = QRect(int(knob_x), int(knob_y), knob_size, knob_size)
        painter.setBrush(QColor(TEXT_PRIMARY))
        painter.drawEllipse(knob_rect)

        text_rect = QRect(track_rect.right() + 10, 0, self.width() - track_rect.right() - 10, self.height())
        painter.setPen(QColor(TEXT_SECONDARY))
        painter.setFont(self.font())
        painter.drawText(text_rect, Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft, self.text())

    def sizeHint(self):
        return self.fontMetrics().size(0, self.text() or "Toggle")


def make_section_label(text: str) -> QLabel:
    label = QLabel(text)
    label.setObjectName("SectionLabel")
    return label


def log_line_to_html(message: str) -> str:
    lower = message.lower()
    if any(key in lower for key in ("error", "failed", "unable to")):
        dot_color, text_color = "#FF4B3E", "#FF9A90"
    elif any(key in lower for key in (
        "updated successfully", "up to date", "finished moving",
        "finished successfully", "success",
    )):
        dot_color, text_color = ACCENT, TEXT_PRIMARY
    else:
        dot_color, text_color = TEXT_MUTED, TEXT_SECONDARY

    timestamp = time.strftime("%H:%M:%S")
    escaped = html.escape(message)
    return (
        f'<span style="color:{TEXT_MUTED};">[{timestamp}]</span> '
        f'<span style="color:{dot_color};">&#9679;</span> '
        f'<span style="color:{text_color};">{escaped}</span>'
    )


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("EZ YT-DLP")
        self.resize(900, 620)
        self.setMinimumSize(760, 540)

        icon_path = get_app_icon_path()
        if icon_path.exists():
            self.setWindowIcon(QIcon(str(icon_path)))

        self.exe_folder = get_exe_folder()
        self.ytdlp_path = self.exe_folder / "yt-dlp.exe"
        self.downloads_folder = Path.home() / "Downloads"
        self.is_running = False
        self.config = load_config()
        if self.config.get("download_path"):
            self.downloads_folder = Path(self.config["download_path"])

        self.download_thread = None
        self.update_thread = None

        self._build_ui()
        QTimer.singleShot(250, self.check_for_updates)

    def _build_ui(self) -> None:
        central = QWidget()
        root_layout = QHBoxLayout(central)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)

        root_layout.addWidget(self._build_sidebar())

        self.stack = QStackedWidget()
        self.stack.addWidget(self._build_download_page())
        self.stack.addWidget(self._build_settings_page())
        root_layout.addWidget(self.stack, 1)

        self.setCentralWidget(central)
        self._update_bitrate_visibility()

    def _build_sidebar(self) -> QFrame:
        sidebar = QFrame()
        sidebar.setObjectName("Sidebar")
        sidebar.setFixedWidth(190)

        layout = QVBoxLayout(sidebar)
        layout.setContentsMargins(16, 20, 12, 16)
        layout.setSpacing(2)

        title = QLabel("EZ YT-DLP")
        title.setObjectName("SidebarTitle")
        subtitle = QLabel(f"v{APP_VERSION}")
        subtitle.setObjectName("SidebarSubtitle")
        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addSpacing(14)

        self.nav_group = QButtonGroup(self)
        self.nav_group.setExclusive(True)

        self.nav_download_btn = QPushButton("Download")
        self.nav_settings_btn = QPushButton("Settings")
        for btn, index in ((self.nav_download_btn, 0), (self.nav_settings_btn, 1)):
            btn.setObjectName("NavButton")
            btn.setCheckable(True)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.clicked.connect(lambda _checked, i=index: self.stack.setCurrentIndex(i))
            self.nav_group.addButton(btn)
            layout.addWidget(btn)

        self.nav_download_btn.setChecked(True)
        layout.addStretch(1)
        return sidebar

    def _build_download_page(self) -> QWidget:
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(28, 26, 28, 24)
        layout.setSpacing(14)

        layout.addWidget(self._page_title("Download"))

        layout.addWidget(make_section_label("Video URL"))
        self.url_entry = QLineEdit()
        self.url_entry.setPlaceholderText("https://www.youtube.com/watch?v=...")
        layout.addWidget(self.url_entry)

        options_row = QGridLayout()
        options_row.setHorizontalSpacing(16)
        options_row.setVerticalSpacing(6)

        options_row.addWidget(make_section_label("Mode"), 0, 0)
        options_row.addWidget(make_section_label("Quality"), 0, 1)
        self.bitrate_section_label = make_section_label("Bitrate")
        options_row.addWidget(self.bitrate_section_label, 0, 2)

        self.mode_combo = QComboBox()
        self.mode_combo.addItems(["Video", "Audio only"])
        self.mode_combo.setCurrentText(self.config.get("default_mode", "Video"))
        self.mode_combo.currentTextChanged.connect(self._update_bitrate_visibility)
        options_row.addWidget(self.mode_combo, 1, 0)

        self.quality_combo = QComboBox()
        self.quality_combo.addItems(["240p", "480p", "720p", "1080p", "Best"])
        self.quality_combo.setCurrentText(self.config.get("default_quality", "Best"))
        options_row.addWidget(self.quality_combo, 1, 1)

        self.bitrate_combo = QComboBox()
        self.bitrate_combo.addItems(["128k", "192k", "320k"])
        self.bitrate_combo.setCurrentText(self.config.get("default_bitrate", "320k"))
        options_row.addWidget(self.bitrate_combo, 1, 2)

        layout.addLayout(options_row)

        button_row = QHBoxLayout()
        self.download_button = QPushButton("Download")
        self.download_button.setObjectName("PrimaryButton")
        self.download_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.download_button.clicked.connect(self.start_download)
        button_row.addWidget(self.download_button)
        button_row.addStretch(1)
        layout.addLayout(button_row)

        layout.addWidget(self._build_console(), 1)
        return page

    def _build_console(self) -> QFrame:
        frame = QFrame()
        frame.setObjectName("ConsoleFrame")
        outer = QVBoxLayout(frame)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(0)

        header = QFrame()
        header.setObjectName("ConsoleHeader")
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(12, 8, 12, 8)

        console_title = QLabel("CONSOLE")
        console_title.setObjectName("ConsoleTitle")
        header_layout.addWidget(console_title)
        header_layout.addStretch(1)

        self.console_status = QLabel("\u25CF Idle")
        self.console_status.setObjectName("ConsoleStatus")
        self.console_status.setStyleSheet(f"color:{TEXT_MUTED};")
        header_layout.addWidget(self.console_status)

        outer.addWidget(header)

        self.console = QTextEdit()
        self.console.setObjectName("Console")
        self.console.setReadOnly(True)
        outer.addWidget(self.console, 1)
        return frame

    def _build_settings_page(self) -> QWidget:
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(28, 26, 28, 24)
        layout.setSpacing(14)

        layout.addWidget(self._page_title("Settings"))

        layout.addWidget(make_section_label("Download path"))
        path_row = QHBoxLayout()
        self.download_path_entry = QLineEdit(self.config.get("download_path", str(self.downloads_folder)))
        browse_btn = QPushButton("Browse")
        browse_btn.setObjectName("SecondaryButton")
        browse_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        browse_btn.clicked.connect(self._browse_download_path)
        path_row.addWidget(self.download_path_entry, 1)
        path_row.addWidget(browse_btn)
        layout.addLayout(path_row)

        defaults_row = QGridLayout()
        defaults_row.setHorizontalSpacing(16)
        defaults_row.setVerticalSpacing(6)

        defaults_row.addWidget(make_section_label("Default mode"), 0, 0)
        defaults_row.addWidget(make_section_label("Default quality"), 0, 1)
        defaults_row.addWidget(make_section_label("Default bitrate"), 0, 2)

        self.settings_mode_combo = QComboBox()
        self.settings_mode_combo.addItems(["Video", "Audio only"])
        self.settings_mode_combo.setCurrentText(self.config.get("default_mode", "Video"))
        defaults_row.addWidget(self.settings_mode_combo, 1, 0)

        self.settings_quality_combo = QComboBox()
        self.settings_quality_combo.addItems(["240p", "480p", "720p", "1080p", "Best"])
        self.settings_quality_combo.setCurrentText(self.config.get("default_quality", "Best"))
        defaults_row.addWidget(self.settings_quality_combo, 1, 1)

        self.settings_bitrate_combo = QComboBox()
        self.settings_bitrate_combo.addItems(["128k", "192k", "320k"])
        self.settings_bitrate_combo.setCurrentText(self.config.get("default_bitrate", "320k"))
        defaults_row.addWidget(self.settings_bitrate_combo, 1, 2)

        layout.addLayout(defaults_row)

        self.skip_updates_checkbox = ToggleSwitch("Skip update prompt")
        self.skip_updates_checkbox.setChecked(bool(self.config.get("skip_update_prompt", False)))
        layout.addWidget(self.skip_updates_checkbox)

        button_row = QHBoxLayout()
        save_btn = QPushButton("Save settings")
        save_btn.setObjectName("PrimaryButton")
        save_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        save_btn.clicked.connect(self._save_settings)

        reset_btn = QPushButton("Reset to defaults")
        reset_btn.setObjectName("SecondaryButton")
        reset_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        reset_btn.clicked.connect(self._reset_settings)

        button_row.addWidget(save_btn)
        button_row.addWidget(reset_btn)
        button_row.addStretch(1)
        layout.addLayout(button_row)
        layout.addStretch(1)
        return page

    @staticmethod
    def _page_title(text: str) -> QLabel:
        label = QLabel(text)
        label.setObjectName("PageTitle")
        return label

    def _update_bitrate_visibility(self, *_args) -> None:
        show_bitrate = self.mode_combo.currentText() == "Audio only"
        self.bitrate_section_label.setVisible(show_bitrate)
        self.bitrate_combo.setVisible(show_bitrate)

    def _browse_download_path(self) -> None:
        folder = QFileDialog.getExistingDirectory(
            self, "Select download folder", self.download_path_entry.text() or str(self.downloads_folder)
        )
        if folder:
            self.download_path_entry.setText(folder)

    def _save_settings(self) -> None:
        self.config["download_path"] = self.download_path_entry.text().strip() or str(self.downloads_folder)
        self.config["default_mode"] = self.settings_mode_combo.currentText() or "Video"
        self.config["default_quality"] = self.settings_quality_combo.currentText() or "Best"
        self.config["default_bitrate"] = self.settings_bitrate_combo.currentText() or "320k"
        self.config["skip_update_prompt"] = bool(self.skip_updates_checkbox.isChecked())
        save_config(self.config)

        self.mode_combo.setCurrentText(self.config["default_mode"])
        self.quality_combo.setCurrentText(self.config["default_quality"])
        self.bitrate_combo.setCurrentText(self.config["default_bitrate"])
        self.downloads_folder = Path(self.config["download_path"])
        self._update_bitrate_visibility()

        QMessageBox.information(self, "Settings saved", "Your settings have been saved.")

    def _reset_settings(self) -> None:
        default_download_path = str(Path.home() / "Downloads")
        self.download_path_entry.setText(default_download_path)
        self.settings_mode_combo.setCurrentText("Video")
        self.settings_quality_combo.setCurrentText("Best")
        self.settings_bitrate_combo.setCurrentText("320k")
        self.skip_updates_checkbox.setChecked(False)

        self.config = {
            "download_path": default_download_path,
            "default_mode": "Video",
            "default_quality": "Best",
            "default_bitrate": "320k",
            "skip_update_prompt": False,
        }
        save_config(self.config)

        self.mode_combo.setCurrentText(self.config["default_mode"])
        self.quality_combo.setCurrentText(self.config["default_quality"])
        self.bitrate_combo.setCurrentText(self.config["default_bitrate"])
        self.downloads_folder = Path(self.config["download_path"])
        self._update_bitrate_visibility()

        QMessageBox.information(self, "Settings reset", "Default settings have been restored.")

    def log_message(self, message: str) -> None:
        self.console.moveCursor(QTextCursor.MoveOperation.End)
        self.console.insertHtml(log_line_to_html(message) + "<br>")
        self.console.moveCursor(QTextCursor.MoveOperation.End)

    def _set_console_running(self, running: bool) -> None:
        if running:
            self.console_status.setText("\u25CF Running")
            self.console_status.setStyleSheet(f"color:{ACCENT};")
        else:
            self.console_status.setText("\u25CF Idle")
            self.console_status.setStyleSheet(f"color:{TEXT_MUTED};")

    # update checker
    def check_for_updates(self) -> None:
        self.update_thread = UpdateCheckThread(
            self.ytdlp_path, bool(self.skip_updates_checkbox.isChecked())
        )
        self.update_thread.log.connect(self.log_message)
        self.update_thread.app_update_found.connect(self._prompt_for_program_update)
        self.update_thread.start()

    def _prompt_for_program_update(self, latest_tag: str, release_url: str) -> None:
        answer = QMessageBox.question(
            self,
            "Update available",
            f"A newer EZ YT-DLP release is available: {latest_tag}\n\nOpen the releases page to download it?",
        )
        if answer == QMessageBox.StandardButton.Yes:
            webbrowser.open(release_url)

    # download
    def _persist_config(self) -> None:
        self.config["skip_update_prompt"] = bool(self.skip_updates_checkbox.isChecked())
        self.config["default_mode"] = self.mode_combo.currentText() or "Video"
        self.config["default_quality"] = self.quality_combo.currentText() or "Best"
        self.config["default_bitrate"] = self.bitrate_combo.currentText() or "320k"
        self.config["download_path"] = self.download_path_entry.text().strip() or str(self.downloads_folder)
        save_config(self.config)

    def start_download(self) -> None:
        if self.is_running:
            return

        url = self.url_entry.text().strip()
        if not url:
            QMessageBox.critical(self, "Missing URL", "Please enter a video URL.")
            return
        if not is_valid_url(url):
            QMessageBox.critical(self, "Invalid URL", "Please enter a valid http:// or https:// URL.")
            return
        if not self.ytdlp_path.exists():
            QMessageBox.critical(self, "Missing yt-dlp", "yt-dlp.exe was not found next to the program.")
            return

        self._persist_config()
        self.is_running = True
        self.download_button.setEnabled(False)
        self.console.clear()
        self._set_console_running(True)
        self.log_message("Starting download...")

        self.download_thread = DownloadThread(
            self.ytdlp_path,
            self.exe_folder,
            self.downloads_folder,
            url,
            self.mode_combo.currentText(),
            self.quality_combo.currentText(),
            self.bitrate_combo.currentText(),
        )
        self.download_thread.log.connect(self.log_message)
        self.download_thread.finished_download.connect(self._finish_download)
        self.download_thread.start()

    def _finish_download(self) -> None:
        self.is_running = False
        self.download_button.setEnabled(True)
        self._set_console_running(False)


def apply_dark_palette(app: QApplication) -> None:
    palette = QPalette()
    palette.setColor(QPalette.ColorRole.Window, QColor(BG_MAIN))
    palette.setColor(QPalette.ColorRole.WindowText, QColor(TEXT_PRIMARY))
    palette.setColor(QPalette.ColorRole.Base, QColor(BG_PANEL))
    palette.setColor(QPalette.ColorRole.AlternateBase, QColor(BG_MAIN))
    palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(TEXT_PRIMARY))
    palette.setColor(QPalette.ColorRole.ToolTipText, QColor(TEXT_PRIMARY))
    palette.setColor(QPalette.ColorRole.Text, QColor(TEXT_PRIMARY))
    palette.setColor(QPalette.ColorRole.Button, QColor(BG_MAIN))
    palette.setColor(QPalette.ColorRole.ButtonText, QColor(TEXT_PRIMARY))
    palette.setColor(QPalette.ColorRole.BrightText, QColor(ACCENT))
    palette.setColor(QPalette.ColorRole.Highlight, QColor(ACCENT))
    palette.setColor(QPalette.ColorRole.HighlightedText, QColor(TEXT_PRIMARY))
    app.setPalette(palette)


def main() -> None:
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    apply_dark_palette(app)
    app.setStyleSheet(STYLESHEET)
    app.setFont(QFont("Segoe UI", 9))

    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()