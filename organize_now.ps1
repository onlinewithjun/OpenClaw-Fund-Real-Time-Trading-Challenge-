$desktop = "C:\Users\Administrator\Desktop"
Write-Host "正在整理桌面文件..."

# 获取桌面所有文件
$files = Get-ChildItem -Path $desktop -File

# 分类移动
$moved = 0
foreach ($file in $files) {
    $name = $file.Name
    $ext = $file.Extension.ToLower()
    
    # 跳过脚本文件本身
    if ($name -eq "organize_now.ps1") { continue }
    
    $destination = $null
    
    # 压缩文件
    if ($ext -in @('.rar', '.zip', '.7z')) {
        $destination = Join-Path $desktop "Compressed"
    }
    # 补丁文件
    elseif ($ext -in @('.patch', '.diff.txt')) {
        $destination = Join-Path $desktop "Patches"
    }
    # 文档
    elseif ($ext -in @('.md', '.docx', '.txt', '.html', '.htm')) {
        $destination = Join-Path $desktop "Documents"
    }
    # 可执行文件
    elseif ($ext -in @('.exe', '.msi')) {
        $destination = Join-Path $desktop "Executables"
    }
    # 快捷方式
    elseif ($ext -eq '.lnk') {
        $destination = Join-Path $desktop "Shortcuts"
    }
    # 其他
    else {
        $destination = Join-Path $desktop "Others"
    }
    
    if ($destination -and (Test-Path $destination)) {
        Write-Host "移动: $name -> $destination"
        Move-Item -Path $file.FullName -Destination $destination -Force
        $moved++
    } else {
        Write-Host "警告: 找不到目标文件夹 $destination"
    }
}

Write-Host "整理完成！共移动了 $moved 个文件。"