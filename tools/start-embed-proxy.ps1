$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
$script = Join-Path $root 'tools\dashscope-embed-proxy.mjs'
$node = (Get-Command node).Source

# Kill old proxy on port 18890 (best effort)
try {
  $conn = Get-NetTCPConnection -LocalPort 18890 -State Listen -ErrorAction SilentlyContinue
  if ($conn) {
    $pids = $conn | Select-Object -ExpandProperty OwningProcess -Unique
    foreach ($pid in $pids) { Stop-Process -Id $pid -Force -ErrorAction SilentlyContinue }
  }
} catch {}

Start-Process -FilePath $node -ArgumentList @($script) -WorkingDirectory $root -WindowStyle Hidden
Write-Output 'embed-proxy started on 127.0.0.1:18890'
