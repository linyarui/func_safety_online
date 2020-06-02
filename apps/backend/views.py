from flask import views, session, request
from flask import render_template, redirect, url_for
from apps.backend import backend
from apps.backend.models import BackendUser
from apps.backend.forms import LoginForm
from config import config


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


backend.add_url_rule('/login/', view_func=LoginView.as_view('login'))
