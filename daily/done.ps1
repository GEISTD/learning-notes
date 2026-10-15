# 确认完成今日计划：归档 → 推送 GitHub dailyPlan → 删除桌面文件 → 推进题号
# 由桌面「✅完成今日计划.vbs」静默调用，结果通过 Toast 反馈
$ErrorActionPreference = "Continue"
$dir = $PSScriptRoot
$py = "C:\Users\29681\AppData\Local\Programs\Python\Python313\python.exe"
if (-not (Test-Path $py)) { $py = "py" }
$repo = "D:\GEIST\dailyPlan"
$stamp = Get-Date -Format "yyyy-MM-dd"
if (-not (Test-Path (Join-Path $dir "logs"))) { New-Item -ItemType Directory -Path (Join-Path $dir "logs") | Out-Null }
$log = Join-Path $dir "logs\$stamp.log"

# 1) Python 结算：pending → done、移动 plans/ → done/、删桌面文件、推进题号与连续打卡
# 与 run_daily.ps1 共用一把互斥锁，防止确认与开机生成并发写 state.json
$rr = $null
$mtx = New-Object System.Threading.Mutex($false, "Local\AIPlanDailyRun")
$locked = $false
try {
    $locked = $mtx.WaitOne(15000)
    if (-not $locked) {
        Add-Content $log "mutex busy"
        $l1 = "生成任务正在运行，请 1 分钟后再点确认"
        $l2 = ""
    } else {
        & $py -X utf8 (Join-Path $dir "gen_daily.py") --confirm *>> $log
    }
}
catch {
    Add-Content $log "confirm failed: $_"
}
finally {
    if ($locked) { $mtx.ReleaseMutex() | Out-Null }
    $mtx.Dispose()
}

# 结果从 Python 直写的 UTF-8 文件读取（不解析子进程 stdout，规避 GBK 乱码）
if (-not $l1) {
    try {
        $rr = [IO.File]::ReadAllText((Join-Path $dir "last_run.json"), [Text.Encoding]::UTF8) | ConvertFrom-Json
    } catch { Add-Content $log "last_run read failed: $_" }
}

if ($l1) {
    # 互斥锁忙，文案已就绪，直接弹 Toast
} elseif ($null -eq $rr) {
    $l1 = "确认失败，详见日志"
    $l2 = "logs\$stamp.log"
} elseif ($rr.result -eq "nothing_pending") {
    $l1 = "没有待确认的计划"
    $l2 = "完成今天的计划后再点确认哦"
} elseif ($rr.result -eq "confirmed") {
    $dates = @($rr.dates)
    $n = $dates.Count
    $streak = $rr.streak
    $l1 = "已确认完成，$n 份计划已归档"
    # 2) 提交并推送归档（失败只记日志，下次自动补推）
    $pushed = $false
    try {
        if (Test-Path (Join-Path $repo ".git")) {
            Push-Location $repo
            git add -A
            git commit -m "done: $($dates -join ' ')" *>> $log
            git push origin main *>> $log
            $pushed = ($LASTEXITCODE -eq 0)
            Pop-Location
        }
    } catch {
        Add-Content $log "git failed: $_"
        try { Pop-Location } catch {}
    }
    if ($pushed) { $l2 = "已推送 GitHub dailyPlan ｜ 连续打卡 $streak 天" }
    else { $l2 = "本地已归档（推送失败，下次自动补推）｜ 连续打卡 $streak 天" }
} else {
    $l1 = "确认失败，详见日志"
    $l2 = "logs\$stamp.log"
}

# 3) Toast 反馈
try {
    [void][Windows.UI.Notifications.ToastNotificationManager, Windows.UI.Notifications, ContentType=WindowsRuntime]
    $tpl = [Windows.UI.Notifications.ToastNotificationManager]::GetTemplateContent([Windows.UI.Notifications.ToastTemplateType]::ToastText02)
    $t = $tpl.GetElementsByTagName("text")
    $t.Item(0).AppendChild($tpl.CreateTextNode($l1)) | Out-Null
    if ($l2) { $t.Item(1).AppendChild($tpl.CreateTextNode($l2)) | Out-Null }
    $toast = [Windows.UI.Notifications.ToastNotification]::new($tpl)
    [Windows.UI.Notifications.ToastNotificationManager]::CreateToastNotifier("AI Daily Plan").Show($toast)
} catch {
    Add-Content $log "toast failed: $_"
}
