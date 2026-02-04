#!/bin/bash

echo "=== 批量创建软链接工具 ==="
echo "这个脚本会把源目录下的所有子文件夹，软链接到目标目录。"
echo "如果目标目录已有同名项，会跳过（不覆盖）。"
echo ""

# 解析命令行参数
source_arg=""
target_arg=""
yes_arg=false

while [[ "$#" -gt 0 ]]; do
  case $1 in
    -s|--source) source_arg="$2"; shift ;;
    -t|--target) target_arg="$2"; shift ;;
    -y|--yes) yes_arg=true ;;
    *) echo "未知参数: $1"; exit 1 ;;
  esac
  shift
done

# 1. 输入源路径
if [ -n "$source_arg" ]; then
  source_root="$source_arg"
  echo "使用命令行参数源路径: $source_root"
else
  echo "请输入源文件夹路径（里面直接是各个 skill 子文件夹，例如："
  echo "   /Users/mac/Desktop/Ai_Skills/superpowers/skills ）"
  read -p "源路径: " source_root
fi

# 去掉可能存在的引号（拖拽文件夹时会自动加引号）
source_root="${source_root#\'}"
source_root="${source_root%\'}"
source_root="${source_root#\"}"
source_root="${source_root%\"}"

# 去掉可能的尾部斜杠，并检查是否为空
source_root="${source_root%/}"
if [ -z "$source_root" ]; then
  echo "错误：源路径不能为空，请重新运行并输入路径。"
  exit 1
fi

# 检查源路径是否存在且是目录
if [ ! -d "$source_root" ]; then
  echo "错误：源路径不存在或不是目录 → $source_root"
  echo "请检查路径是否正确（可以用 Finder 复制路径）"
  exit 1
fi

echo "源路径已确认: $source_root"
echo ""

# 2. 输入目标路径（提供默认值）
default_target="$HOME/.agents/skills"

if [ -n "$target_arg" ]; then
  target_dir="$target_arg"
  echo "使用命令行参数目标路径: $target_dir"
else
  echo "请输入目标文件夹路径（软链接会创建在这里）"
  echo "默认: $default_target"
  read -p "目标路径 (按回车使用默认): " target_dir
fi

# 如果没输入，用默认
if [ -z "$target_dir" ]; then
  target_dir="$default_target"
fi

# 去掉可能存在的引号
target_dir="${target_dir#\'}"
target_dir="${target_dir%\'}"
target_dir="${target_dir#\"}"
target_dir="${target_dir%\"}"

target_dir="${target_dir%/}"

# 自动创建目标目录（如果不存在）
mkdir -p "$target_dir"
if [ ! -d "$target_dir" ]; then
  echo "错误：无法创建或访问目标目录 → $target_dir"
  exit 1
fi

echo "目标路径已确认: $target_dir"
echo ""

# 3. 确认执行
echo "即将执行："
echo "  把 $source_root 下的所有子目录"
echo "  软链接到 $target_dir"
echo "  （同名跳过）"

if [ "$yes_arg" = true ]; then
  echo "静默模式：自动确认执行。"
else
  read -p "确认开始？ (y/n): " confirm
  if [[ ! "$confirm" =~ ^[Yy] ]]; then
    echo "已取消。"
    exit 0
  fi
fi

# 4. 开始创建链接
cd "$target_dir" || exit 1

created_list=()
skipped_list=()

echo ">> 正在扫描并创建链接..."

for skill_dir in "$source_root"/*/; do
  [ -d "$skill_dir" ] || continue
  
  skill_name=$(basename "$skill_dir")
  
  if [ -e "$skill_name" ]; then
    skipped_list+=("$skill_name")
    continue
  fi
  
  ln -s "$skill_dir" "$skill_name"
  created_list+=("$skill_name")
done

# 5. 总结 (现代 CLI 风格)
echo ""
echo "========================================"
echo "           执行结果汇总           "
echo "========================================"

if [ ${#created_list[@]} -gt 0 ]; then
  echo -e "\033[1;32m✅  新增链接 (${#created_list[@]}):\033[0m"
  for name in "${created_list[@]}"; do
    echo "   + $name"
  done
else
  echo "✨  没有新增链接"
fi

echo ""

if [ ${#skipped_list[@]} -gt 0 ]; then
  echo -e "\033[1;33m⏭️  已存在/跳过 (${#skipped_list[@]}):\033[0m"
  # 如果跳过的太多，可以只显示前几个
  if [ ${#skipped_list[@]} -gt 10 ]; then
     for ((i=0; i<10; i++)); do
       echo "   • ${skipped_list[$i]}"
     done
     echo "   ... (以及其他 $((${#skipped_list[@]} - 10)) 个)"
  else
     for name in "${skipped_list[@]}"; do
       echo "   • $name"
     done
  fi
else
  echo "✨  没有跳过的项"
fi

echo ""
echo "----------------------------------------"
echo "📂 目标目录: $target_dir"
echo "🎉 完成！"
echo ""