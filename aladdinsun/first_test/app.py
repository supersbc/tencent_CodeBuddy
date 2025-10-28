from flask import Flask, render_template, request, jsonify
import sqlite3
from datetime import datetime
from contextlib import contextmanager

app = Flask(__name__)

# 数据库文件路径
DATABASE = 'todos.db'

def init_db():
    """初始化数据库"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS todos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT NOT NULL,
            completed INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

@contextmanager
def get_db():
    """获取数据库连接的上下文管理器"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()

def load_todos():
    """加载所有待办事项"""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM todos ORDER BY id DESC')
        rows = cursor.fetchall()
        return [dict(row) for row in rows]

@app.route('/')
def index():
    """主页"""
    return render_template('index.html')

@app.route('/api/todos', methods=['GET'])
def get_todos():
    """获取所有待办事项"""
    todos = load_todos()
    # 转换 completed 为布尔值，created_at 为 createdAt
    for todo in todos:
        todo['completed'] = bool(todo['completed'])
        todo['createdAt'] = todo.pop('created_at')
    return jsonify(todos)

@app.route('/api/todos', methods=['POST'])
def add_todo():
    """添加待办事项"""
    data = request.get_json()
    text = data.get('text', '').strip()
    
    if not text:
        return jsonify({'error': '待办事项不能为空'}), 400
    
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO todos (text, completed, created_at) VALUES (?, ?, ?)',
            (text, 0, datetime.now().isoformat())
        )
        conn.commit()
        todo_id = cursor.lastrowid
        
        cursor.execute('SELECT * FROM todos WHERE id = ?', (todo_id,))
        row = cursor.fetchone()
        new_todo = dict(row)
        new_todo['completed'] = bool(new_todo['completed'])
        new_todo['createdAt'] = new_todo.pop('created_at')
    
    return jsonify(new_todo), 201

@app.route('/api/todos/<int:todo_id>', methods=['PUT'])
def update_todo(todo_id):
    """更新待办事项"""
    data = request.get_json()
    
    with get_db() as conn:
        cursor = conn.cursor()
        
        # 检查待办事项是否存在
        cursor.execute('SELECT * FROM todos WHERE id = ?', (todo_id,))
        if not cursor.fetchone():
            return jsonify({'error': '待办事项不存在'}), 404
        
        # 更新字段
        if 'completed' in data:
            cursor.execute(
                'UPDATE todos SET completed = ? WHERE id = ?',
                (1 if data['completed'] else 0, todo_id)
            )
        if 'text' in data:
            cursor.execute(
                'UPDATE todos SET text = ? WHERE id = ?',
                (data['text'], todo_id)
            )
        
        conn.commit()
        
        # 返回更新后的数据
        cursor.execute('SELECT * FROM todos WHERE id = ?', (todo_id,))
        row = cursor.fetchone()
        todo = dict(row)
        todo['completed'] = bool(todo['completed'])
        todo['createdAt'] = todo.pop('created_at')
    
    return jsonify(todo)

@app.route('/api/todos/<int:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    """删除待办事项"""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM todos WHERE id = ?', (todo_id,))
        conn.commit()
    return jsonify({'message': '删除成功'})

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """获取统计信息"""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) as total FROM todos')
        total = cursor.fetchone()['total']
        
        cursor.execute('SELECT COUNT(*) as active FROM todos WHERE completed = 0')
        active = cursor.fetchone()['active']
        
        cursor.execute('SELECT COUNT(*) as completed FROM todos WHERE completed = 1')
        completed = cursor.fetchone()['completed']
    
    return jsonify({
        'total': total,
        'active': active,
        'completed': completed
    })

if __name__ == '__main__':
    init_db()  # 初始化数据库
    app.run(debug=True, host='0.0.0.0', port=5001)
