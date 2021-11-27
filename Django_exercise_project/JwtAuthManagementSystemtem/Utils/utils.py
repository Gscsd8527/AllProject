

def resp_success_status(msg: str, **data) -> dict:
    """
    返回成功
    :param msg:
    :param data:
    :return:
    """
    if data and data != {}:
        return {
            'code': 200,
            'message': f'{msg} 成功',
            'data': data
        }
    else:
        return {
            'code': 200,
            'message': f'{msg} 成功',
        }

def resp_error_status(msg: str) -> dict:
    """
    返回失败
    :param msg:
    :return:
    """
    return {
        'code': 300,
        'message': msg,
    }


def jwt_response_payload_handler(token, user=None, request=None, role=None):
    """
    自定义jwt认证成功返回数据
    :token  返回的jwt
    :user   当前登录的用户信息[对象]
    :request 当前本次客户端提交过来的数据
    :role 角色
    """
    if user.first_name:
        name = user.first_name
    else:
        name = user.username
    print('AAA= ', {
        "authenticated": 'true',
        'id': user.id,
        'name': name,
        'username': user.username,
        'email': user.email,
        'token': token,
    })
    return {
        "authenticated": 'true',
        'id': user.id,
        'name': name,
        'username': user.username,
        'email': user.email,
        'token': token,
    }

