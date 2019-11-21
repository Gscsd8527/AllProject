
CLIENT_ID = 'aa87fb3bd529581eac5b'

CLIENT_SECRET = '3ff3e7d7413b27b309aec717fecb04ccb30eef47'

CLIENT_CALLBACK_URL = 'http://127.0.0.1:8000/oauth/'  #填写你的回调地址

def main():
    github = 'https://github.com/login/oauth/authorize'
    auth_url = github + '?client_id={}&redirect_url={}'.format(CLIENT_ID, CLIENT_CALLBACK_URL)
    print(auth_url)
if __name__ == '__main__':
    main()