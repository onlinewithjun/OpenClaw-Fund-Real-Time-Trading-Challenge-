$desktop = Join-Path $env:USERPROFILE "Desktop"
Write-Host "桌面路径: $desktop"

# 创建分类文件夹
$folders = @("Compressed", "Patches", "Documents", "Executables", "Shortcuts", "Others")
foreach ($folder in $folders) {
    $path = Join-Path $desktop $folder
    if (-not (Test-Path $path)) {
        New-Item -Path $path -ItemType Directory -Force | Out-Null
        Write-Host "创建文件夹: $folder"
    }
}

# 获取桌面文件（排除刚创建的文件夹）
$files = Get-ChildItem -Path $desktop -File

# 分类规则
$compressedExt = @('.rar', '.zip', '.7z')
$patchesExt = @('.patch', '.diff.txt')
$documentsExt = @('.md', '.docx', '.txt', '.html', '.htm')
$executablesExt = @('.exe', '.msi')
$shortcutsExt = @('.lnk')

foreach ($file in $files) {
    $ext = $file.Extension.ToLower()
    $destination = $null
    
    if ($compressedExt -contains $ext) {
        $destination = Join-Path $desktop "Compressed"
    }
    elseif ($patchesExt -contains $ext) {
        $destination = Join-Path $desktop "Patches"
    }
    elseif ($documentsExt -contains $ext) {
        $destination = Join-Path $desktop "Documents"
    }
    elseif ($executablesExt -contains $ext) {
        $destination = Join-Path $desktop "Executables"
    }
    elseif ($shortcutsExt -contains $ext) {
        $destination = Join-Path $desktop "Shortcuts"
    }
    else {
        $destination = Join-Path $desktop "Others"
    }
    
    if ($destination) {
        Write-Host "移动: $($file.Name) -> $destination"
        # 实际移动前先注释掉Move-Item，只显示计划
        # Move-Item -Path $file.FullName -Destination $destination -Force
    }
}

Write-Host "`n整理完成！"