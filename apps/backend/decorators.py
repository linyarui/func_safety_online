from flask import session, redirect, url_for
from config import config
from functools import wraps


# 登录验证装饰器
def login_required(func):
    @wraps(func)
    def inner(*args, **kwargs):
        if config['development'].BACKEND_USER_ID in session:
            return func(*args, **kwargs)
        return redirect(url_for('backend.login'))

    return inner
