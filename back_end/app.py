from flask import send_from_directory
from APP import create_app
from APP.extends import db
app = create_app()
@app.route("/")
def Hello():
    return "hello world"


if __name__ == '__main__':
    app.run(debug=False)
    # debug自动重启 port端口 host 127.0.0.1默认 0.0.0.0本机所有ip
