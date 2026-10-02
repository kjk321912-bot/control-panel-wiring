param([string]$Path)
Add-Type -AssemblyName System.Runtime.WindowsRuntime
$null=[Windows.Storage.StorageFile,Windows.Storage,ContentType=WindowsRuntime]
$null=[Windows.Media.Ocr.OcrEngine,Windows.Foundation,ContentType=WindowsRuntime]
$null=[Windows.Graphics.Imaging.BitmapDecoder,Windows.Graphics,ContentType=WindowsRuntime]
$asTask=([System.WindowsRuntimeSystemExtensions].GetMethods()|?{$_.Name -eq 'AsTask' -and $_.GetParameters().Count -eq 1 -and $_.GetParameters()[0].ParameterType.Name -eq 'IAsyncOperation`1'})[0]
function Await($op,[Type]$t){$task=$asTask.MakeGenericMethod($t).Invoke($null,@($op));$task.Wait()|Out-Null;$task.Result}
$f=Await ([Windows.Storage.StorageFile]::GetFileFromPathAsync($Path)) ([Windows.Storage.StorageFile])
$s=Await ($f.OpenAsync([Windows.Storage.FileAccessMode]::Read)) ([Windows.Storage.Streams.IRandomAccessStream])
$dec=Await ([Windows.Graphics.Imaging.BitmapDecoder]::CreateAsync($s)) ([Windows.Graphics.Imaging.BitmapDecoder])
$bmp=Await ($dec.GetSoftwareBitmapAsync()) ([Windows.Graphics.Imaging.SoftwareBitmap])
$null=[Windows.Globalization.Language,Windows.Globalization,ContentType=WindowsRuntime]
$lang=[Windows.Globalization.Language]::new("en-US")
$eng=[Windows.Media.Ocr.OcrEngine]::TryCreateFromLanguage($lang)
if(-not $eng){$eng=[Windows.Media.Ocr.OcrEngine]::TryCreateFromUserProfileLanguages()}
"max "+[Windows.Media.Ocr.OcrEngine]::MaxImageDimension
$r=Await ($eng.RecognizeAsync($bmp)) ([Windows.Media.Ocr.OcrResult])
foreach($l in $r.Lines){foreach($w in $l.Words){ "{0}`t{1:0}`t{2:0}`t{3:0}`t{4:0}" -f $w.Text,$w.BoundingRect.X,$w.BoundingRect.Y,$w.BoundingRect.Width,$w.BoundingRect.Height }}
