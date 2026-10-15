# 每日计划生成（登录时 / 08:30 由任务计划调用）
# 补确认弹窗（有遗留时） → 生成 → Toast → 推送新计划到 GitHub dailyPlan 仓库
$ErrorActionPreference = "Continue"
# 子进程（python -X utf8）输出按 UTF-8 解码，否则中文系统默认 GBK 会把捕获结果变成乱码
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8
$dir = $PSScriptRoot
$py = "C:\Users\29681\AppData\Local\Programs\Python\Python313\python.exe"
if (-not (Test-Path $py)) { $py = "py" }

# 单实例互斥锁：开机时 ONLOGON 与 08:30 两个任务可能并发触发，
# 第二个实例直接退出，避免重复弹窗、重复生成（拿到锁的实例负责全部流程）
$mtx = New-Object System.Threading.Mutex($false, "Local\AIPlanDailyRun")
if (-not $mtx.WaitOne(5000)) { exit }

$stamp = Get-Date -Format "yyyy-MM-dd"
if (-not (Test-Path (Join-Path $dir "logs"))) { New-Item -ItemType Directory -Path (Join-Path $dir "logs") | Out-Null }
$log = Join-Path $dir "logs\$stamp.log"

try {
# 0) 补确认弹窗：有未确认的遗留计划且今天还没生成过 → 先问"完成了没"
#    [是] 归档遗留并按新题号生成  [否]/超时(10分钟) → 延续同一题
$statusOut = & $py -X utf8 (Join-Path $dir "gen_daily.py") --status 2>> $log
$carry = ($statusOut | Select-String "^CARRY:(.+)").Matches.Groups[1].Value
$todayEntry = ($statusOut | Select-String "^TODAY_ENTRY:(\w+)").Matches.Groups[1].Value
if ($carry -and $carry -ne "none" -and $todayEntry -eq "no") {
    try {
        $ws = New-Object -ComObject WScript.Shell
        $r = $ws.Popup("检测到之前（$carry）的计划还没确认完成。`n`n[是] 我已完成 → 归档并生成新题`n[否] 没完成 → 今天继续同一题`n（10 分钟无操作默认未完成）", 600, "每日计划 · 昨日确认", 4 + 48)
        if ($r -eq 6) {
            & $py -X utf8 (Join-Path $dir "gen_daily.py") --confirm --past-only *>> $log
            Add-Content $log "popup-confirmed: past plans archived"
        } else {
            Add-Content $log "popup-answer: $r (carry over)"
        }
    } catch {
        Add-Content $log "popup failed: $_"
    }
}

# 1) 生成计划与练习文件（幂等：同一天重复运行不重复出题；今天已确认则结果为 today_done）
& $py -X utf8 (Join-Path $dir "gen_daily.py") *>> $log
$todayDone = $false
try {
    $rr = [IO.File]::ReadAllText((Join-Path $dir "last_run.json"), [Text.Encoding]::UTF8) | ConvertFrom-Json
    $todayDone = ($rr.result -eq "today_done")
} catch { Add-Content $log "last_run read failed: $_" }

# 2) Toast 通知（原生 WinRT，无需安装模块；今天已确认归档则不再打扰）
if (-not $todayDone) {
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
}

# 3) 推送新计划到 GitHub dailyPlan 仓库（失败只记日志，下次自动补推）
try {
    $repo = "D:\GEIST\dailyPlan"
    if (Test-Path (Join-Path $repo ".git")) {
        Push-Location $repo
        $dirty = git status --porcelain
        if ($dirty) {
            git add -A
            git commit -m "plan: $stamp" *>> $log
            git push origin main *>> $log
        }
        Pop-Location
    }
} catch {
    Add-Content $log "git failed: $_"
    try { Pop-Location } catch {}
}
}
finally {
    $mtx.ReleaseMutex() | Out-Null
    $mtx.Dispose()
}
