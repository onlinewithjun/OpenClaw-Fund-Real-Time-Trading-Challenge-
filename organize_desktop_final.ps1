# 桌面整理脚本
# 请先确认分类方案，然后取消注释Move-Item行以实际移动文件

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
$files = Get-ChildItem -Path $desktop -File | Where-Object { $_.Extension -ne "" }

# 分类规则
$compressedExt = @('.rar', '.zip', '.7z')
$patchesExt = @('.patch', '.diff.txt')
$documentsExt = @('.md', '.docx', '.txt', '.html', '.htm')
$executablesExt = @('.exe', '.msi')
$shortcutsExt = @('.lnk')

$movedCount = 0

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
        # 是否移动快捷方式？根据参数决定
        if ($args[0] -eq "MoveShortcuts") {
            $destination = Join-Path $desktop "Shortcuts"
        } else {
            Write-Host "跳过快捷方式: $($file.Name) (保留在桌面)"
            continue
        }
    }
    else {
        $destination = Join-Path $desktop "Others"
    }
    
    if ($destination) {
        Write-Host "移动: $($file.Name) -> $destination"
        # 取消注释下一行以实际移动文件
        # Move-Item -Path $file.FullName -Destination $destination -Force
        $movedCount++
    }
}

Write-Host "`n整理完成！计划移动 $movedCount 个文件。"
Write-Host "要实际移动文件，请取消脚本中Move-Item行的注释。"