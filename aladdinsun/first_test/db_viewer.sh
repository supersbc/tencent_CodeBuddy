#!/bin/bash
# SQLite 数据库查看脚本

DB_FILE="todos.db"

echo "========================================="
echo "  待办事项数据库查看器"
echo "========================================="
echo ""

# 查看所有待办事项
echo "📋 所有待办事项："
sqlite3 $DB_FILE <<EOF
.mode table
.headers on
SELECT 
    id as ID,
    text as 内容,
    CASE completed WHEN 0 THEN '❌ 未完成' ELSE '✅ 已完成' END as 状态,
    created_at as 创建时间
FROM todos
ORDER BY id DESC;
EOF

echo ""
echo "========================================="

# 统计信息
echo "📊 统计信息："
sqlite3 $DB_FILE <<EOF
.mode table
.headers on
SELECT 
    COUNT(*) as 总数,
    SUM(CASE WHEN completed = 0 THEN 1 ELSE 0 END) as 未完成,
    SUM(CASE WHEN completed = 1 THEN 1 ELSE 0 END) as 已完成
FROM todos;
EOF

echo ""
echo "========================================="
