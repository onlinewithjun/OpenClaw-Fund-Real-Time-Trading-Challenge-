Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing

$screen = [System.Windows.Forms.Screen]::PrimaryScreen
$bounds = $screen.Bounds

$bitmap = New-Object System.Drawing.Bitmap $bounds.Width, $bounds.Height
$graphics = [System.Drawing.Graphics]::FromImage($bitmap)
$graphics.CopyFromScreen($bounds.Location, [System.Drawing.Point]::Empty, $bounds.Size)
$graphics.Dispose()

$screenshotPath = Join-Path 'C:\Users\Administrator\.openclaw\workspace' 'desktop_screenshot.png'
$bitmap.Save($screenshotPath, [System.Drawing.Imaging.ImageFormat]::Png)
$bitmap.Dispose()

Write-Output "Screenshot saved to: $screenshotPath"
if (Test-Path $screenshotPath) {
    Write-Output "File exists: $(Get-Item $screenshotPath | Select-Object Length)"
}