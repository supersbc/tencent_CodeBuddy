from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return '''
    <!DOCTYPE html>
    <html>
    <head><title>测试页面</title></head>
    <body>
        <h1>Flask服务正常运行！</h1>
        <p>如果你能看到这个页面，说明Flask服务工作正常。</p>
    </body>
    </html>
    '''

if __name__ == '__main__':
    print("启动测试服务器...")
    app.run(debug=True, host='0.0.0.0', port=5173)
