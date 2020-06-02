from flask import views, session, request, g
from flask import render_template, redirect, url_for
from flask_mail import Message
from apps.backend import backend
from apps.backend.models import BackendUser
from apps.backend.forms import LoginForm, ResetPwdForm, ResetEmailForm
from apps.backend.decorators import login_required
from apps.utils import xjson, xcache
from config import config
from exts import db, mail
import string
import random


class IndexView(views.MethodView):
    """
    后台主页
    """

    decorators = [login_required]  # 登录验证

    def get(self):
        return render_template('backend/b_index.html')


class LoginView(views.MethodView):
    """
    后台管理员登录
    """

    def _render(self, message):
        return render_template('backend/b_login.html', message=message)

    def get(self, message=None):
        return self._render(message)

    def post(self):
        login_form = LoginForm(request.form)
        if login_form.validate():
            email = login_form.email.data
            password = login_form.password.data
            remember = login_form.remember.data
            user = BackendUser.query.filter_by(email=email).first()
            if user and user.check_password(password):
                session[config['development'].BACKEND_USER_ID] = user.id
                if remember:
                    session.permanent = True
                next_url = request.args.get('next')
                if not next_url or not next_url.startswith('/backend/'):
                    return redirect(url_for('backend.index'))
                return redirect(next_url)
            return self._render(message='账号或密码错误')
        message = login_form.get_error()
        return self._render(message=message)


class LogoutView(views.MethodView):
    """
    登出
    """
    decorators = [login_required]

    def get(self):
        session.pop(config['development'].BACKEND_USER_ID)
        return redirect(url_for('backend.login'))


class ProfileView(views.MethodView):
    """
    个人信息
    """
    decorators = [login_required]

    def get(self):
        return render_template('backend/b_profile.html')


class ResetPwdView(views.MethodView):
    """
    修改密码
    """
    decorators = [login_required]

    def get(self):
        return render_template('backend/b_resetpwd.html')

    def post(self):
        reset_pwd_form = ResetPwdForm(request.form)
        if reset_pwd_form.validate():
            old_pwd = reset_pwd_form.old_pwd.data
            new_pwd = reset_pwd_form.new_pwd.data
            user = g.backend_user
            if user.check_password(old_pwd):
                user.password = new_pwd
                db.session.commit()
                return xjson.json_success('密码修改成功')
            return xjson.json_params_error('原密码输入错误')
        message = reset_pwd_form.get_error()
        return xjson.json_params_error(message)


class EmailCaptcha(views.MethodView):
    """
    发送邮箱验证码
    """
    decorators = [login_required]

    def get(self):
        email = request.args.get('email')
        if not email:
            return xjson.json_params_error('请输入邮件参数')

        # 生成6位随机验证码
        source = list(string.ascii_letters)
        source.extend(map(lambda x: str(x), range(0, 10)))
        captcha = ''.join(random.sample(source, 6))

        # 发送邮件
        msg = Message('功能安全性系统邮箱验证码', recipients=[email],
                      body='您的验证码：{}，5分钟内有效'.format(captcha))

        try:
            mail.send(msg)
        except Exception as err:
            print(err)
            return xjson.json_server_error(message='邮件发送失败')

        # 验证码存入memcached
        xcache.set(email, captcha)
        return xjson.json_success(message='邮件发送成功')


class ResetEmailView(views.MethodView):
    """
    修改邮箱
    """
    decorators = [login_required]

    def get(self):
        return render_template('backend/b_resetemail.html')

    def post(self):
        reset_email_form = ResetEmailForm(request.form)
        if reset_email_form.validate():
            email = reset_email_form.email.data
            g.backend_user.email = email
            db.session.commit()
            return xjson.json_success('邮箱修改成功')
        message = reset_email_form.get_error()
        return xjson.json_params_error(message)


backend.add_url_rule('/index/', view_func=IndexView.as_view('index'))
backend.add_url_rule('/login/', view_func=LoginView.as_view('login'))
backend.add_url_rule('/logout/', view_func=LogoutView.as_view('logout'))
backend.add_url_rule('/profile/', view_func=ProfileView.as_view('profile'))
backend.add_url_rule('/resetpwd/', view_func=ResetPwdView.as_view('resetpwd'))
backend.add_url_rule('/email_captcha/', view_func=EmailCaptcha.as_view('email_captcha'))
backend.add_url_rule('/resetemail/', view_func=ResetEmailView.as_view('resetemail'))
