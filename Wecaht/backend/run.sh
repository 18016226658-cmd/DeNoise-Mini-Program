#!/bin/bash

echo "启动大整数分解系统后端..."
echo ""

# 检查 Python 是否安装
if ! command -v python3 &> /dev/null; then
    echo "错误: 未找到 Python，请先安装 Python 3.8+"
    exit 1
fi

# 检查依赖是否安装
echo "检查依赖..."
if ! python3 -c "import flask" 2>/dev/null; then
    echo "正在安装依赖..."
    pip3 install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "错误: 依赖安装失败"
        exit 1
    fi
fi

# 运行应用
echo "启动 Flask 应用..."
python3 app.py

