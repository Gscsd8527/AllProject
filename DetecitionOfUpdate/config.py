import logging
logger = logging.getLogger(__name__)
logger.setLevel(level=logging.INFO)
handler = logging.FileHandler("log.txt")
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

HOST = "smtp.163.com"  # 设置发件服务器地址
# mail_user = "******"  # 用户名
# mail_pass = "******"  # 口令
SENDER = '******'  # 设置发件邮箱，一定要自己注册的邮箱
PWD = '******'  # 设置发件邮箱的授权码密码，根据163邮箱提示，登录第三方邮件客户端需要授权码