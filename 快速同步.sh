#!/bin/bash
# 快速同步到 GitHub 和工蜂

cd /data/workspace/tencent_CodeBuddy

echo "======================================"
echo "  🚀 快速同步到 GitHub & 工蜂"
echo "======================================"
echo ""

# 检查是否有未提交的更改
if [ -n "$(git status --porcelain)" ]; then
    echo "📝 检测到未提交的更改:"
    git status --short | head -10
    echo ""
    read -p "📋 请输入提交信息: " msg
    
    if [ -n "$msg" ]; then
        git add .
        git commit -m "$msg"
        echo "✅ 代码已提交"
    else
        echo "❌ 提交取消"
        exit 1
    fi
fi

echo ""
echo "📤 推送到 GitHub..."
if git push origin main 2>&1 | tail -3; then
    echo "✅ GitHub 推送成功"
else
    echo "❌ GitHub 推送失败"
fi

echo ""
echo "📤 推送到工蜂..."
if git push gongfeng main 2>&1 | tail -3; then
    echo "✅ 工蜂推送成功"
else
    echo "❌ 工蜂推送失败"
fi

echo ""
echo "======================================"
echo "  ✨ 同步完成!"
echo "======================================"
echo ""
echo "📊 仓库地址:"
echo "  GitHub: https://github.com/supersbc/tencent_CodeBuddy"
echo "  工蜂:   https://git.woa.com/aladdinsun/AIdatabase"
echo ""
