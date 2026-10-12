# 晚间自动提交：把当天手写的练习答案 commit + push（23:00 任务计划调用）
$ErrorActionPreference = "Continue"
$dir = $PSScriptRoot
$stamp = Get-Date -Format "yyyy-MM-dd"
$log = Join-Path $dir "logs\$stamp.log"

try {
    $repo = Split-Path $dir -Parent
    Push-Location $repo
    $dirty = git status --porcelain -- daily
    if ($dirty) {
        git add daily/
        git commit -m "docs(daily): handwritten practice $stamp" *>> $log
        git push origin main *>> $log
        Add-Content $log "evening commit done"
    } else {
        Add-Content $log "evening: nothing to commit"
    }
    Pop-Location
} catch {
    Add-Content $log "evening git failed: $_"
    try { Pop-Location } catch {}
}
