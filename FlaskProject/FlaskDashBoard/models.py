from exts import db
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(50), unique=True)

    def __init__(self, email, username, password):  # 类似与java中的构造器
        self.email = email
        self.username = username
        self.password = password

    def set_password(self, password):  # 对明文密码进行加密，返回的是加密后的密码
        return generate_password_hash(password)

    def check_password(self, password):  # 检查密码，传入的是明文密码，会将明文密码进行加密后再进行比对
        return check_password_hash(self.password, password)

    def change_password(self, password):  # 修改密码
        self.password = self.set_password(password)
