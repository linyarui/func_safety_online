from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from apps import create_app
from exts import db
# from apps.front.models import *
# from apps.backend.models import BackendUser

app = create_app()

manager = Manager(app)
Migrate(app, db)
manager.add_command('db', MigrateCommand)

# @manager.option('-u', '--username', dest='username')
# @manager.option('-p', '--password', dest='password')
# @manager.option('-e', '--email', dest='email')
# def create_admin_user(username, password, email):
#     user = BackendUser(username=username, password=password, email=email)
#     db.session.add(user)
#     db.session.commit()
#     print('后台管理员用户创建成功')


if __name__ == '__main__':
    manager.run()
