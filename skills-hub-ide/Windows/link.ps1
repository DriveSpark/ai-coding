# =========================================
# 批量创建符号链接工具 (Windows 版)
# =========================================

param(
    [string]$Source,
    [string]$Target,
    [switch]$Yes,
    [switch]$Help
)

# 设置控制台编码为 UTF-8
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
[Console]::InputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8

Write-Host "=== 批量创建符号链接工具 ===" -ForegroundColor Cyan
Write-Host "这个脚本会把源目录下的所有子文件夹，符号链接到目标目录。"
Write-Host "如果目标目录已有同名项，会跳过（不覆盖）。"
Write-Host ""

# 显示帮助
if ($Help) {
    Write-Host "用法: .\link.ps1 [选项]"
    Write-Host ""
    Write-Host "选项:"
    Write-Host "  -Source <path>   源文件夹路径 (包含各个 skill 子目录)"
    Write-Host "  -Target <path>   目标文件夹路径 (符号链接将被创建在此)"
    Write-Host "  -Yes             静默模式 (自动确认，不进行交互询问)"
    Write-Host "  -Help            显示此帮助信息"
    Write-Host ""
    Write-Host "示例:"
    Write-Host "  .\link.ps1                                          # 交互式运行"
    Write-Host "  .\link.ps1 -Source .\my-skills -Target C:\skills    # 命令行运行"
    exit 0
}

# 1. 输入源路径
if ($Source) {
    $sourceRoot = $Source
    Write-Host "使用命令行参数源路径: $sourceRoot"
} else {
    Write-Host "请输入源文件夹路径（里面直接是各个 skill 子文件夹）"
    $sourceRoot = Read-Host "源路径"
}

# 去掉可能存在的引号
$sourceRoot = $sourceRoot.Trim('"').Trim("'").TrimEnd('\').TrimEnd('/')

if ([string]::IsNullOrWhiteSpace($sourceRoot)) {
    Write-Host "错误：源路径不能为空，请重新运行并输入路径。" -ForegroundColor Red
    exit 1
}

# 检查源路径是否存在且是目录
if (-not (Test-Path -Path $sourceRoot -PathType Container)) {
    Write-Host "错误：源路径不存在或不是目录 → $sourceRoot" -ForegroundColor Red
    Write-Host "请检查路径是否正确"
    exit 1
}

Write-Host "源路径已确认: $sourceRoot" -ForegroundColor Green
Write-Host ""

# 2. 输入目标路径
if ($Target) {
    $targetDir = $Target
    Write-Host "使用命令行参数目标路径: $targetDir"
} else {
    Write-Host "请输入目标文件夹路径（符号链接会创建在这里）"
    $targetDir = Read-Host "目标路径"
}

# 去掉可能存在的引号
$targetDir = $targetDir.Trim('"').Trim("'").TrimEnd('\').TrimEnd('/')

if ([string]::IsNullOrWhiteSpace($targetDir)) {
    Write-Host "错误：目标路径不能为空" -ForegroundColor Red
    exit 1
}

# 自动创建目标目录（如果不存在）
if (-not (Test-Path -Path $targetDir)) {
    try {
        New-Item -ItemType Directory -Path $targetDir -Force | Out-Null
        Write-Host "已创建目标目录: $targetDir" -ForegroundColor Yellow
    } catch {
        Write-Host "错误：无法创建目标目录 → $targetDir" -ForegroundColor Red
        exit 1
    }
}

Write-Host "目标路径已确认: $targetDir" -ForegroundColor Green
Write-Host ""

# 3. 确认执行
Write-Host "即将执行："
Write-Host "  把 $sourceRoot 下的所有子目录"
Write-Host "  符号链接到 $targetDir"
Write-Host "  （同名跳过）"

if ($Yes) {
    Write-Host "静默模式：自动确认执行。" -ForegroundColor Yellow
} else {
    $confirm = Read-Host "确认开始？ (y/n)"
    if ($confirm -notmatch '^[Yy]') {
        Write-Host "已取消。"
        exit 0
    }
}

# 4. 开始创建链接
$createdList = @()
$skippedList = @()
$errorList = @()

Write-Host ""
Write-Host ">> 正在扫描并创建链接..." -ForegroundColor Cyan

$skillDirs = Get-ChildItem -Path $sourceRoot -Directory

foreach ($skillDir in $skillDirs) {
    $skillName = $skillDir.Name
    $linkPath = Join-Path -Path $targetDir -ChildPath $skillName
    
    if (Test-Path -Path $linkPath) {
        $skippedList += $skillName
        continue
    }
    
    try {
        # 使用 cmd /c mklink /D 创建目录符号链接 (需要管理员权限)
        # 或者使用 New-Item -ItemType SymbolicLink (PowerShell 5.0+, 需要管理员权限)
        # 这里使用 Junction (不需要管理员权限)
        cmd /c mklink /J "$linkPath" "$($skillDir.FullName)" 2>&1 | Out-Null
        
        if ($LASTEXITCODE -eq 0) {
            $createdList += $skillName
        } else {
            # 尝试使用 SymbolicLink (可能需要管理员权限)
            try {
                New-Item -ItemType SymbolicLink -Path $linkPath -Target $skillDir.FullName -ErrorAction Stop | Out-Null
                $createdList += $skillName
            } catch {
                $errorList += $skillName
            }
        }
    } catch {
        $errorList += $skillName
    }
}

# 5. 总结
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "           执行结果汇总           " -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

if ($createdList.Count -gt 0) {
    Write-Host "✅  新增链接 ($($createdList.Count)):" -ForegroundColor Green
    foreach ($name in $createdList) {
        Write-Host "   + $name" -ForegroundColor Green
    }
} else {
    Write-Host "✨  没有新增链接"
}

Write-Host ""

if ($skippedList.Count -gt 0) {
    Write-Host "⏭️  已存在/跳过 ($($skippedList.Count)):" -ForegroundColor Yellow
    if ($skippedList.Count -gt 10) {
        for ($i = 0; $i -lt 10; $i++) {
            Write-Host "   • $($skippedList[$i])" -ForegroundColor Yellow
        }
        Write-Host "   ... (以及其他 $($skippedList.Count - 10) 个)" -ForegroundColor Yellow
    } else {
        foreach ($name in $skippedList) {
            Write-Host "   • $name" -ForegroundColor Yellow
        }
    }
} else {
    Write-Host "✨  没有跳过的项"
}

if ($errorList.Count -gt 0) {
    Write-Host ""
    Write-Host "❌  创建失败 ($($errorList.Count)):" -ForegroundColor Red
    foreach ($name in $errorList) {
        Write-Host "   ! $name" -ForegroundColor Red
    }
    Write-Host ""
    Write-Host "提示：创建符号链接可能需要管理员权限，请尝试以管理员身份运行 PowerShell" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "----------------------------------------"
Write-Host "📂 目标目录: $targetDir" -ForegroundColor Cyan
Write-Host "🎉 完成！" -ForegroundColor Green
Write-Host ""
