#!/bin/bash

# 自动获取当前脚本所在目录
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
CORE_SCRIPT="$SCRIPT_DIR/link.sh"

# 检查核心脚本是否存在
if [ ! -f "$CORE_SCRIPT" ]; then
  echo "❌ 错误：脚本缺少执行文件，未找到核心脚本 -> $CORE_SCRIPT"
  echo "请确保 skills_manager.sh 和 link.sh 在同一目录下。"
  exit 1
fi

# 配置路径
HUB_PATH="$HOME/.agents/skills"

# 动态获取 SOURCE_PATH
echo "请输入源文件夹路径（您的真实 Skills 源码库，支持拖拽）："
read -p "源路径: " SOURCE_PATH

# 处理引号
SOURCE_PATH="${SOURCE_PATH#\'}"
SOURCE_PATH="${SOURCE_PATH%\'}"
SOURCE_PATH="${SOURCE_PATH#\"}"
SOURCE_PATH="${SOURCE_PATH%\"}"
# 去掉可能的尾部斜杠
SOURCE_PATH="${SOURCE_PATH%/}"

# 检查源路径
if [ -z "$SOURCE_PATH" ] || [ ! -d "$SOURCE_PATH" ]; then
  echo "❌ 错误：源路径为空或不存在 -> $SOURCE_PATH"
  exit 1
fi

# IDE 目标路径配置 (请确认)
IDE_PATHS=(
  "Trae:$HOME/.trae/skills"
  "Antigravity:$HOME/.gemini/antigravity/global_skills"
)

echo "=== 🚀 AI Skills 全局分发系统 ==="
echo ""

# ---------------------------------------------------------
# 第一阶段：同步 Source -> Hub
# ---------------------------------------------------------
echo ">> 正在同步 Source -> Hub 中转站..."
echo "Source: $SOURCE_PATH"
echo "Hub:    $HUB_PATH"
echo ""

# 调用核心脚本 (静默模式)
"$CORE_SCRIPT" -s "$SOURCE_PATH" -t "$HUB_PATH" -y

if [ $? -ne 0 ]; then
  echo "❌ Source -> Hub 同步失败，请检查错误。"
  exit 1
fi
echo "✅ Hub 中转站同步完成！"
echo "---------------------------------------------------------"

# ---------------------------------------------------------
# 第二阶段：分发 Hub -> IDEs (多选交互 - 方向键控制)
# ---------------------------------------------------------
echo ""
echo ">> 准备分发到各个 IDE..."

# 初始化选中状态 (全部未选中)
selected=()
for ((i=0; i<${#IDE_PATHS[@]}; i++)); do
  selected[i]=false
done

# 当前光标位置
current=0

# 隐藏光标
tput civis

# 恢复光标函数
cleanup() {
  tput cnorm
}
trap cleanup EXIT

# 绘制菜单函数
draw_menu() {
  # 移动光标回到菜单起始位置 (根据列表长度向上移动)
  # 注意：这里需要根据实际打印行数调整
  # 简单起见，我们每次清屏重画
  clear
  echo "=== 请选择要同步的目标 IDE ==="
  echo "↑/↓: 移动光标 | 空格: 选中/取消 | 回车: 确认执行 | ESC/q: 退出"
  echo ""

  # 显示临时消息
  if [ -n "$flash_msg" ]; then
    echo -e "$flash_msg"
    flash_msg="" # 显示一次后清除
  else
    echo "" # 占位符，保持布局稳定
  fi
  
  # 收集已选中的项
  selected_names=""
  for ((i=0; i<${#IDE_PATHS[@]}; i++)); do
    if [ "${selected[i]}" = true ]; then
      item="${IDE_PATHS[$i]}"
      name="${item%%:*}"
      if [ -z "$selected_names" ]; then
        selected_names="$name"
      else
        selected_names="$selected_names, $name"
      fi
    fi
  done

  # 打印当前选中状态
  if [ -z "$selected_names" ]; then
    echo "当前选中: (无)"
  else
    echo -e "当前选中: \033[1;32m$selected_names\033[0m"
  fi
  echo "----------------------------------------"
  
  for ((i=0; i<${#IDE_PATHS[@]}; i++)); do
    item="${IDE_PATHS[$i]}"
    name="${item%%:*}"
    path="${item#*:}"
    
    # 选中标记
    if [ "${selected[i]}" = true ]; then
      mark="\033[1;32m●\033[0m" # 绿色圆点
    else
      mark="○"
    fi
    
    # 光标标记
    if [ $i -eq $current ]; then
      prefix="\033[1;36m> \033[0m" # 青色箭头
      line_style="\033[1m" # 加粗当前行
      reset_style="\033[0m"
    else
      prefix="  "
      line_style=""
      reset_style=""
    fi
    
    echo -e "${prefix}${mark} ${line_style}${name}${reset_style} -> ${path}"
  done
}

# 交互循环
while true; do
  draw_menu
  
  # 读取按键 (兼容不同终端)
  IFS= read -rsn1 key
  if [[ "$key" == $'\x1b' ]]; then
    IFS= read -rsn2 -t 0.1 key
    if [[ "$key" == "[A" ]]; then
      # Up
      ((current--))
      if [ $current -lt 0 ]; then current=$((${#IDE_PATHS[@]} - 1)); fi
    elif [[ "$key" == "[B" ]]; then
      # Down
      ((current++))
      if [ $current -ge ${#IDE_PATHS[@]} ]; then current=0; fi
    elif [[ -z "$key" ]]; then
      # ESC key press (without follow-up codes)
      echo ""
      echo "已退出。"
      exit 0
    fi
  elif [[ "$key" == " " ]]; then
    # Space (Toggle)
    if [ "${selected[current]}" = true ]; then
      selected[current]=false
    else
      selected[current]=true
    fi
  elif [[ "$key" == "" ]]; then
    # Enter
    # 检查是否至少选择了一个
    has_selection=false
    for ((i=0; i<${#IDE_PATHS[@]}; i++)); do
      if [ "${selected[i]}" = true ]; then
        has_selection=true
        break
      fi
    done
    
    if [ "$has_selection" = true ]; then
      break
    else
      # 显示提示信息（不退出循环）
      # 这里我们可以闪烁一下或者打印提示，但因为马上会重绘，所以我们可以在 draw_menu 里加状态，或者简单的 sleep 一下
      # 为了简单，我们可以在菜单上方加一个临时错误提示，或者直接在 draw_menu 里处理
      # 这里我们采用一个简单的方式：不退出，继续循环。
      # 为了让用户感知，我们可以设置一个临时消息变量
      flash_msg="\033[1;31m⚠️  请至少选择一个目标 IDE！\033[0m"
      continue
    fi
  elif [[ "$key" == "q" ]]; then
    echo ""
    echo "已退出。"
    exit 0
  fi
done

# 恢复光标
tput cnorm

# 收集最终选中的索引
selected_indices=()
for ((i=0; i<${#IDE_PATHS[@]}; i++)); do
  if [ "${selected[i]}" = true ]; then
    selected_indices+=($i)
  fi
done

# 检查是否未选
if [ ${#selected_indices[@]} -eq 0 ]; then
  echo ""
  echo "⚠️ 您没有选择任何目标 IDE，跳过分发步骤。"
  echo "🎉 任务结束。"
  exit 0
fi

# 执行分发
echo ""
echo ">> 开始同步选中的 ${#selected_indices[@]} 个目标..."
for idx in "${selected_indices[@]}"; do
  item="${IDE_PATHS[$idx]}"
  name="${item%%:*}"
  target_path="${item#*:}"
  
  echo ""
  echo ">> 正在分发给 $name ..."
  
  # 调用核心脚本 (静默模式)
  # 注意：这里 Source 变成了 Hub
  "$CORE_SCRIPT" -s "$HUB_PATH" -t "$target_path" -y
  
  if [ $? -eq 0 ]; then
    echo "✅ $name 同步成功！"
  else
    echo "⚠️ $name 同步遇到问题。"
  fi
done

echo ""
echo "🎉 所有任务执行完毕！"
