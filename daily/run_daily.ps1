# 每日计划生成（登录时 / 08:30 由任务计划调用）
# 不硬编码中文路径：全部相对 $PSScriptRoot
$ErrorActionPreference = "Continue"
$dir = $PSScriptRoot
$py = "C:\Users\29681\AppData\Local\Programs\Python\Python313\python.exe"
if (-not (Test-Path $py)) { $py = "py" }

$stamp = Get-Date -Format "yyyy-MM-dd"
$log = Join-Path $dir "logs\$stamp.log"
if (-not (Test-Path (Join-Path $dir "logs"))) { New-Item -ItemType Directory -Path (Join-Path $dir "logs") | Out-Null }

# 1) 生成计划与练习文件
& $py -X utf8 (Join-Path $dir "gen_daily.py") *>> $log

# 2) Toast 通知（原生 WinRT，无需安装模块；失败则静默跳过）
try {
    [void][Windows.UI.Notifications.ToastNotificationManager, Windows.UI.Notifications, ContentType=WindowsRuntime]
    $tpl = [Windows.UI.Notifications.ToastNotificationManager]::GetTemplateContent([Windows.UI.Notifications.ToastTemplateType]::ToastText02)
    $sumFile = Join-Path $dir "last_summary.txt"
    if (Test-Path $sumFile) {
        $lines = Get-Content $sumFile -Encoding UTF8
        $t = $tpl.GetElementsByTagName("text")
        $t.Item(0).AppendChild($tpl.CreateTextNode($lines[0])) | Out-Null
        if ($lines.Count -gt 1) { $t.Item(1).AppendChild($tpl.CreateTextNode($lines[1])) | Out-Null }
    }
    $toast = [Windows.UI.Notifications.ToastNotification]::new($tpl)
    [Windows.UI.Notifications.ToastNotificationManager]::CreateToastNotifier("AI Daily Plan").Show($toast)
} catch {
    Add-Content $log "toast failed: $_"
}

# 3) 自动提交并推送（失败只记日志，不弹窗打扰）
try {
    $repo = Split-Path $dir -Parent
    Push-Location $repo
    $dirty = git status --porcelain -- daily
    if ($dirty) {
        git add daily/
        git commit -m "chore(daily): $stamp plan + practice scaffold" *>> $log
        git push origin main *>> $log
    }
    Pop-Location
} catch {
    Add-Content $log "git failed: $_"
    try { Pop-Location } catch {}
}
