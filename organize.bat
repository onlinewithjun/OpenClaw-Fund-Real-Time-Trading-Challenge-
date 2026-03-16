@echo off
chdir /d "%USERPROFILE%\Desktop"
echo 正在整理桌面文件...

REM 创建文件夹（如果已存在会跳过）
if not exist "Compressed" mkdir Compressed
if not exist "Patches" mkdir Patches
if not exist "Documents" mkdir Documents
if not exist "Executables" mkdir Executables
if not exist "Shortcuts" mkdir Shortcuts
if not exist "Others" mkdir Others

REM 移动压缩文件
if exist "*.rar" move *.rar Compressed\
if exist "*.zip" move *.zip Compressed\
if exist "*.7z" move *.7z Compressed\

REM 移动补丁文件
if exist "*.patch" move *.patch Patches\
if exist "*.diff.txt" move *.diff.txt Patches\

REM 移动文档文件
if exist "*.md" move *.md Documents\
if exist "*.docx" move *.docx Documents\
if exist "*.txt" move *.txt Documents\
if exist "*.html" move *.html Documents\
if exist "*.htm" move *.htm Documents\

REM 移动可执行文件
if exist "*.exe" move *.exe Executables\
if exist "*.msi" move *.msi Executables\

REM 移动快捷方式
if exist "*.lnk" move *.lnk Shortcuts\

REM 移动其他文件（排除文件夹）
for %%f in (*) do (
    if not "%%~xf"=="" (
        if not exist "%%f\" (
            if not "%%~xf"==".rar" if not "%%~xf"==".zip" if not "%%~xf"==".7z" (
            if not "%%~xf"==".patch" if not "%%~xf"==".diff.txt" (
            if not "%%~xf"==".md" if not "%%~xf"==".docx" if not "%%~xf"==".txt" if not "%%~xf"==".html" if not "%%~xf"==".htm" (
            if not "%%~xf"==".exe" if not "%%~xf"==".msi" (
            if not "%%~xf"==".lnk" (
                echo 移动其他文件: %%f
                move "%%f" Others\
            ))))))
        )
    )
)

echo 整理完成！
pause