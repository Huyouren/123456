from app import create_app, db
from app.models import User, basicinfo, Major
from flask import url_for

app = create_app()

# 添加shell上下文，方便调试
@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, basicinfo=basicinfo, Major=Major)

if __name__ == '__main__':
    app.run(debug=True)