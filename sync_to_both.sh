#!/bin/bash

# ============================================
# GitHub & 工蜂 双仓库同步脚本
# ============================================

set -e

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo "=========================================="
echo "  🔄 GitHub & 工蜂双仓库同步"
echo "=========================================="
echo ""

cd /data/workspace/tencent_CodeBuddy

# 检查是否有未提交的更改
if [ -n "$(git status --porcelain)" ]; then
    echo -e "${YELLOW}⚠️  检测到未提交的更改${NC}"
    git status --short
    echo ""
    read -p "是否提交这些更改? (y/n): " DO_COMMIT
    
    if [ "$DO_COMMIT" = "y" ]; then
        read -p "请输入提交信息: " COMMIT_MSG
        git add .
        git commit -m "$COMMIT_MSG"
        echo -e "${GREEN}✅ 已提交更改${NC}"
    else
        echo -e "${RED}❌ 取消同步${NC}"
        exit 1
    fi
fi

echo ""
echo "📋 当前分支: $(git branch --show-current)"
echo "📝 最新提交: $(git log --oneline -1)"
echo ""

# 推送到 GitHub
echo -e "${YELLOW}📤 推送到 GitHub...${NC}"
if git push origin main; then
    echo -e "${GREEN}✅ GitHub 同步成功!${NC}"
    echo "   仓库地址: https://github.com/supersbc/tencent_CodeBuddy"
else
    echo -e "${RED}❌ GitHub 推送失败${NC}"
fi

echo ""

# 推送到工蜂
echo -e "${YELLOW}📤 推送到工蜂...${NC}"
if git push gongfeng main 2>&1 | tee /tmp/gongfeng_push.log; then
    echo -e "${GREEN}✅ 工蜂同步成功!${NC}"
    echo "   仓库地址: https://git.woa.com/aladdinsun/tencent_CodeBuddy"
else
    if grep -q "Git repository not found" /tmp/gongfeng_push.log; then
        echo -e "${YELLOW}⚠️  工蜂仓库尚未创建${NC}"
        echo ""
        echo "请先在工蜂创建仓库:"
        echo "1. 访问: https://git.woa.com/projects/new"
        echo "2. 项目名称: tencent_CodeBuddy"
        echo "3. 项目路径: aladdinsun/tencent_CodeBuddy"
        echo "4. 可见性: 内部 (Internal)"
        echo "5. 创建后运行: git push gongfeng main"
    else
        echo -e "${RED}❌ 工蜂推送失败${NC}"
        cat /tmp/gongfeng_push.log
    fi
fi

echo ""
echo "=========================================="
echo "  ✨ 同步完成"
echo "=========================================="
echo ""
echo "📊 同步结果:"
echo "  - GitHub:  ✅ https://github.com/supersbc/tencent_CodeBuddy"
echo "  - 工蜂:    需要先创建仓库"
echo ""
