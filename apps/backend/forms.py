from wtforms import StringField, IntegerField
from wtforms.validators import Email, EqualTo, Length, InputRequired, ValidationError
from apps.forms import BaseForm
from apps.backend.models import BackendUser
from apps.utils import xcache


class LoginForm(BaseForm):
    """
    后台登录Form
    """
    email = StringField(validators=[Email(message='邮箱格式错误'), InputRequired(message='请输入邮箱')])
    password = StringField(validators=[Length(6, 20, message='密码长度为6--20')])
    remember = IntegerField()


class ResetPwdForm(BaseForm):
    """
    后台修改密码Form
    """
    old_pwd = StringField(validators=[Length(6, 20, message='密码长度为6--20')])
    new_pwd = StringField(validators=[Length(6, 20, message='密码长度为6--20')])
    new_pwd2 = StringField(validators=[EqualTo('new_pwd', message='两次密码不一致')])


class ResetEmailForm(BaseForm):
    """
    后台修改邮箱
    """
    email = StringField(validators=[Email(message='邮箱格式错误'), InputRequired(message='请输入邮箱')])
    captcha = StringField(validators=[Length(6, 6, message='邮箱验证码长度错误')])

    def validate_email(self, field):
        user = BackendUser.query.filter_by(email=field.data).first()
        if user:
            raise ValidationError('该邮箱已存在')

    def validate_captcha(self, field):
        email = self.email.data
        captcha = field.data
        captcha_cache = xcache.get(email)
        # 判断memcached中是否有对应的邮箱及验证码，小写进行比较，这样用户就不用区分大小写
        if not captcha_cache or captcha.lower() != captcha_cache.lower():
            raise ValidationError('邮箱验证码错误')