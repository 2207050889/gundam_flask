from app import create_app
from flask import redirect, url_for

app = create_app()

# 添加根路由，直接重定向到登录页面
@app.route('/')
def root():
    return redirect(url_for('auth.login'))

print("Flask 启动！")

if __name__ == '__main__':
    app.run(debug=True) 