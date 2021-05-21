import jwt
from jwt import exceptions
def jiami():
    encode_jwt = jwt.encode({'uid':'123'},'密钥123',algorithm='HS256')
    print(encode_jwt)
    # 解密
    encode_jwt = str(encode_jwt, encoding='utf-8')   #  转码强转 必须进行转码
    decode_jwt = jwt.decode(encode_jwt, '密钥123', algorithms=['HS256'])
    print(decode_jwt)  # 字典形式

def miyao():
    a = 'pel4*t5rj&b7_ufu3rw8y%z$^)o(o!==3wv5p98f^+@)txvohd'
    encode_jwt = jwt.encode({'uid': 23}, a, algorithm='HS256')
    encode_jwt = str(encode_jwt, encoding='utf-8')  # 转化为字符串类型
    decode_jwt = jwt.decode(encode_jwt, a, algorithms=['HS256'])  # 解密
    print(decode_jwt)

import datetime
SALT = 'd%=w@)#q7ro(y=j44rwaf4hi-)h5(*a5$ohsy$3!y&u--atr_q'

def create_token():
    """
    生成 token
    :return:
    """
    headers = {
        'typ': 'jwt',
        'alg': 'HS256'
    }
    # 构造payload
    payload = {
        'user_id': 1,  # 自定义用户ID
        'username': 'wupeiqi',  # 自定义用户名
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=1) # 超时时间
    }
    result = jwt.encode(payload=payload, key=SALT, algorithm="HS256", headers=headers).decode('utf-8')
    return result


def get_payload(jwt_token):
    """
    1. 切割
    2. 解密第二段/判断是否过期
    3. 验证第三段合法性
    return:
    """
    try:
        verified_payload = jwt.decode(jwt_token, SALT, True)
        return verified_payload
    except exceptions.ExpiredSignatureError:
        print('token已失效')
    except jwt.DecodeError:
        print('token认证失败')
    except jwt.InvalidTokenError:
        print('非法的token')


def main():
    """
    JWT token 测试
    :return:
    """
    # jiami()
    # miyao()

    # tokent = create_token()
    # print(tokent)
    token = 'eyJ0eXAiOiJqd3QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxLCJ1c2VybmFtZSI6Ind1cGVpcWkiLCJleHAiOjE2MjA5NzU2NDh9.aqP4FXFkO02xgHs2L-xpo6Tj3I3laehagPmZkrYy_24'
    data = get_payload(token)
    print(data)

if __name__ == '__main__':
    main()

