from flask import render_template
from flask_wtf import CSRFProtect
from apps import create_app

app = create_app()
CSRFProtect(app)


# 404 页面
@app.errorhandler(404)
def page_not_fount(error):
    return render_template('system/404.html'), 404


# 500页面
@app.errorhandler(500)
def server_error(error):
    return render_template('system/500.html'), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5500, processes=True)
