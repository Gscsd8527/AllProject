
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
