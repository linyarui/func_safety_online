from wtforms import Form


class BaseForm(Form):
    # 添加获取错误信息的方法
    def get_error(self):
        message = self.errors.popitem()[1][0]
        return message
