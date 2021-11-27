import jwt
import datetime
from django.conf import settings

SALT = settings.SECRET_KEY
# 创建token
def create_token(payload, timeout=1000):
    headers = {
        'typ': 'jwt',
        'alg': 'HS256'
    }
    # 构造payload
    payload['exp'] = datetime.datetime.utcnow() + datetime.timedelta(minutes=timeout)  # 超时时间
    token = jwt.encode(payload=payload, key=SALT, algorithm="HS256", headers=headers).decode('utf-8')
    return token
