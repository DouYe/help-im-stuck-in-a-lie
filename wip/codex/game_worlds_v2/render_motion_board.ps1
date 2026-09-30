# Beat-cut review animatic. Static proposals gain slow camera drift and a
# brief crop-offset impact at each bar. All final scene motion remains a
# proposed production task; this script does not alter the app edit.
$ErrorActionPreference = 'Stop'
$root = "D:\Videos\Help! I'm stuck in a LIE"
$framesDir = Join-Path $root 'design\keyframes\codex_game_worlds_v2'
$manifest = Get-Content -LiteralPath (Join-Path $framesDir 'frames.json') -Raw -Encoding UTF8 | ConvertFrom-Json
$pick = @('01','01','02','03','04','05','06','07','07B','08')
$count = @(73,73,73,36,109,73,73,36,36,73)
$audio = Join-Path $root 'audio\final\song.mp3'
$target = Join-Path $root 'wip\codex\game_worlds_v2\motion_board_work.mp4'
$ff = @('-hide_banner','-loglevel','error','-y')
for ($i = 0; $i -lt $pick.Count; $i++) {
    $item = $manifest | Where-Object { $_.id -eq $pick[$i] } | Select-Object -First 1
    if (-not $item) { throw "Missing frame $($pick[$i])" }
    $path = Join-Path $framesDir $item.file
    $ff += @('-loop','1','-framerate','30','-t',([string]($count[$i]/30.0)),'-i',$path)
}
$ff += @('-i',$audio)

$pieces = @()
for ($i = 0; $i -lt $pick.Count; $i++) {
    if ($i -eq 1) {
        $base = "[$($i):v]scale=2300:1294:flags=lanczos,crop=1920:1080:x=220:y=96"
    } else {
        $base = "[$($i):v]scale=1920:1080:flags=lanczos"
    }
    $pieces += "$base,trim=end_frame=$($count[$i]),setsar=1,setpts=PTS-STARTPTS[v$i]"
}
$links = (0..($pick.Count-1) | ForEach-Object { "[v$_]" }) -join ''
$pieces += "${links}concat=n=$($pick.Count):v=1:a=0[cat]"
# Every 2.424 s is a downbeat. Decaying 0.12-second jitter supplies the
# requested impact while preserving the code glyphs and avoiding flash/glow.
$beat = '(t-2.424*floor(t/2.424))'
$x = "56+12*sin(t*0.9)+14*exp(-18*$beat)*sin(110*$beat)"
$y = "31+7*sin(t*0.7)+9*exp(-18*$beat)*sin(95*$beat)"
$pieces += "[cat]scale=2032:1143:flags=lanczos,crop=1920:1080:x='$x':y='$y',fps=30,format=yuv420p[v]"
$pieces += "[10:a]atrim=start=42.012:duration=21.833333,asetpts=PTS-STARTPTS[a]"
$filter = $pieces -join ';'
$ff += @('-filter_complex',$filter,'-map','[v]','-map','[a]','-c:v','libx264','-preset','fast','-crf','20','-r','30','-c:a','aac','-b:a','192k','-t','21.833333','-movflags','+faststart',$target)
& ffmpeg @ff
if ($LASTEXITCODE -ne 0) { throw "ffmpeg failed: $LASTEXITCODE" }
Write-Output $target
