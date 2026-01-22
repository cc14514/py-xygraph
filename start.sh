#!/bin/bash
set -e

# 定义颜色
GREEN='\033[0;32m'
NC='\033[0m' # No Color

echo -e "${GREEN}🚀 开始启动 py-xygraph...${NC}"

# 1. 检查 Python
if command -v python3 &> /dev/null; then
    PY_CMD=python3
elif command -v python &> /dev/null; then
    PY_CMD=python
else
    echo "❌ 未找到 Python，请先安装 Python 3"
    exit 1
fi

echo "✅ 使用 Python: $($PY_CMD --version)"

# 2. 检查并创建虚拟环境
VENV_DIR="myenv"

if [ ! -d "$VENV_DIR" ]; then
    echo -e "${GREEN}📦 正在创建虚拟环境...${NC}"
    $PY_CMD -m venv $VENV_DIR
    echo "✅ 虚拟环境创建完成"
else
    echo "✅ 虚拟环境已存在"
fi

# 3. 激活虚拟环境
source $VENV_DIR/bin/activate

# 4. 检查并安装依赖
echo -e "${GREEN}📥 正在检查依赖...${NC}"

# 如果有 deps.txt 则使用它
if [ ! -f "deps.txt" ]; then
    echo "matplotlib" > deps.txt
    echo "numpy" >> deps.txt
fi

pip install -r deps.txt

# 5. 启动应用
echo -e "${GREEN}🎨 启动应用程序...${NC}"
python main.py

