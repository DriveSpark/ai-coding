# =========================================
# AI Skills 全局分发系统 (Windows 版)
# 直接从源目录分发到各 IDE 目标目录
# =========================================

# 设置控制台编码为 UTF-8
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
[Console]::InputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8

# 自动获取当前脚本所在目录
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$coreScript = Join-Path -Path $scriptDir -ChildPath "link.ps1"

# 检查核心脚本是否存在
if (-not (Test-Path -Path $coreScript)) {
    Write-Host "❌ 错误：脚本缺少执行文件，未找到核心脚本 -> $coreScript" -ForegroundColor Red
    Write-Host "请确保 skills_manager.ps1 和 link.ps1 在同一目录下。"
    exit 1
}

# IDE 目标路径配置 (Windows 路径)
$idePaths = @(
    @{ Name = "Trae"; Path = "$env:USERPROFILE\.trae\skills" },
    @{ Name = "Antigravity"; Path = "$env:USERPROFILE\.gemini\antigravity\skills" }
)

Write-Host "=== 🚀 AI Skills 全局分发系统 (Windows 版) ===" -ForegroundColor Cyan
Write-Host ""

# ---------------------------------------------------------
# 获取源路径
# ---------------------------------------------------------
Write-Host "请输入源文件夹路径（您的真实 Skills 源码库）：" -ForegroundColor Yellow
$sourcePath = Read-Host "源路径"

# 处理引号和尾部斜杠
$sourcePath = $sourcePath.Trim('"').Trim("'").TrimEnd('\').TrimEnd('/')

# 检查源路径
if ([string]::IsNullOrWhiteSpace($sourcePath) -or -not (Test-Path -Path $sourcePath -PathType Container)) {
    Write-Host "❌ 错误：源路径为空或不存在 -> $sourcePath" -ForegroundColor Red
    exit 1
}

Write-Host "✅ 源路径已确认: $sourcePath" -ForegroundColor Green
Write-Host "---------------------------------------------------------"

# ---------------------------------------------------------
# 选择目标 IDE (方向键交互菜单 - 与 MacOS 一致)
# ---------------------------------------------------------
Write-Host ""
Write-Host ">> 准备分发到各个 IDE..." -ForegroundColor Cyan

# 初始化选中状态 (全部未选中)
$selected = @()
for ($i = 0; $i -lt $idePaths.Count; $i++) {
    $selected += $false
}

# 当前光标位置
$current = 0

# 临时消息
$flashMsg = ""

# 绘制菜单函数
function Draw-Menu {
    Clear-Host
    Write-Host "=== 请选择要同步的目标 IDE ===" -ForegroundColor Cyan
    Write-Host "↑/↓: 移动光标 | 空格: 选中/取消 | 回车: 确认执行 | ESC/q: 退出" -ForegroundColor Gray
    Write-Host ""
    
    # 显示临时消息
    if ($script:flashMsg -ne "") {
        Write-Host $script:flashMsg -ForegroundColor Red
        $script:flashMsg = ""
    } else {
        Write-Host ""
    }
    
    # 收集已选中的项
    $selectedNames = @()
    for ($i = 0; $i -lt $idePaths.Count; $i++) {
        if ($script:selected[$i]) {
            $selectedNames += $idePaths[$i].Name
        }
    }
    
    # 打印当前选中状态
    if ($selectedNames.Count -eq 0) {
        Write-Host "当前选中: (无)"
    } else {
        Write-Host "当前选中: $($selectedNames -join ', ')" -ForegroundColor Green
    }
    Write-Host "----------------------------------------"
    
    # 显示选项列表
    for ($i = 0; $i -lt $idePaths.Count; $i++) {
        $item = $idePaths[$i]
        $name = $item.Name
        $path = $item.Path
        
        # 选中标记
        if ($script:selected[$i]) {
            $mark = "[●]"
            $markColor = "Green"
        } else {
            $mark = "[ ]"
            $markColor = "Gray"
        }
        
        # 光标标记
        if ($i -eq $script:current) {
            Write-Host -NoNewline "  > " -ForegroundColor Cyan
            Write-Host -NoNewline $mark -ForegroundColor $markColor
            Write-Host " $name -> $path" -ForegroundColor White
        } else {
            Write-Host -NoNewline "    "
            Write-Host -NoNewline $mark -ForegroundColor $markColor
            Write-Host " $name -> $path" -ForegroundColor Gray
        }
    }
}

# 交互循环
$running = $true
while ($running) {
    Draw-Menu
    
    # 读取按键
    $key = [Console]::ReadKey($true)
    
    switch ($key.Key) {
        "UpArrow" {
            $current--
            if ($current -lt 0) { $current = $idePaths.Count - 1 }
        }
        "DownArrow" {
            $current++
            if ($current -ge $idePaths.Count) { $current = 0 }
        }
        "Spacebar" {
            $selected[$current] = -not $selected[$current]
        }
        "Enter" {
            # 检查是否至少选择了一个
            $hasSelection = $false
            for ($i = 0; $i -lt $idePaths.Count; $i++) {
                if ($selected[$i]) {
                    $hasSelection = $true
                    break
                }
            }
            
            if ($hasSelection) {
                $running = $false
            } else {
                $flashMsg = "⚠️  请至少选择一个目标 IDE！"
            }
        }
        "Escape" {
            Write-Host ""
            Write-Host "已退出。"
            exit 0
        }
        "Q" {
            Write-Host ""
            Write-Host "已退出。"
            exit 0
        }
    }
}

# 收集最终选中的索引
$selectedIndices = @()
for ($i = 0; $i -lt $idePaths.Count; $i++) {
    if ($selected[$i]) {
        $selectedIndices += $i
    }
}

# 显示选中的目标
Clear-Host
Write-Host "=== 🚀 AI Skills 全局分发系统 (Windows 版) ===" -ForegroundColor Cyan
Write-Host ""
$selectedNames = ($selectedIndices | ForEach-Object { $idePaths[$_].Name }) -join ", "
Write-Host "已选中: $selectedNames" -ForegroundColor Green

# ---------------------------------------------------------
# 直接从源目录分发到各 IDE
# ---------------------------------------------------------
Write-Host ""
Write-Host ">> 开始同步选中的 $($selectedIndices.Count) 个目标..." -ForegroundColor Cyan

foreach ($idx in $selectedIndices) {
    $item = $idePaths[$idx]
    $targetPath = $item.Path
    $name = $item.Name
    
    Write-Host ""
    Write-Host ">> 正在分发给 $name ..." -ForegroundColor Cyan
    Write-Host "   源: $sourcePath"
    Write-Host "   目标: $targetPath"
    
    # 调用核心脚本 (静默模式)
    # 直接从源路径分发到目标路径
    & $coreScript -Source $sourcePath -Target $targetPath -Yes
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ $name 同步成功！" -ForegroundColor Green
    } else {
        Write-Host "⚠️ $name 同步遇到问题。" -ForegroundColor Yellow
    }
}

Write-Host ""
Write-Host "🎉 所有任务执行完毕！" -ForegroundColor Green
