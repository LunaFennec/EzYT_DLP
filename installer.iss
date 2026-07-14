; Inno Setup Script for EZ_YT-DLP
; Build with: iscc installer.iss

#define MyAppName "EZ_YT-DLP"
#ifndef MyAppVersion
#define MyAppVersion "1.4.1"
#endif
#define MyAppPublisher "LunaFennec"
#define MyAppURL "https://github.com/LunaFennec/EzYT_DLP"
#define MyExeName "EZ_YT-DLP.exe"

[Setup]
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
OutputBaseFilename=EZ_YT-DLP-setup
Compression=lzma2
SolidCompression=yes
DisableProgramGroupPage=yes
CreateAppDir=yes
OutputDir=dist\installer
SetupIconFile=icon.ico
PrivilegesRequired=admin

[Tasks]
Name: "desktopicon"; Description: "Create a &desktop icon"; GroupDescription: "Additional icons:"; Flags: unchecked

[Files]
Source: "dist\EZ_YT-DLP.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "icon.ico"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyExeName}"; IconFilename: "{app}\icon.ico"
Name: "{commondesktop}\{#MyAppName}"; Filename: "{app}\{#MyExeName}"; Tasks: desktopicon; IconFilename: "{app}\icon.ico"

[Run]
Filename: "{app}\{#MyExeName}"; Description: "Launch {#MyAppName}"; Flags: nowait postinstall skipifsilent

[UninstallDelete]
Type: filesandordirs; Name: "{app}"
Type: filesandordirs; Name: "{userappdata}\EZ_YT-DLP"
Type: filesandordirs; Name: "{userappdata}\EZ_YT-DLP\*"
Type: filesandordirs; Name: "{localappdata}\EZ_YT-DLP"
Type: filesandordirs; Name: "{localappdata}\EZ_YT-DLP\*"
Type: files; Name: "{userappdata}\yt-dlp.exe"
Type: files; Name: "{userappdata}\ffmpeg.exe"
Type: files; Name: "{userappdata}\ffprobe.exe"
Type: files; Name: "{localappdata}\yt-dlp.exe"
Type: files; Name: "{localappdata}\ffmpeg.exe"
Type: files; Name: "{localappdata}\ffprobe.exe"
