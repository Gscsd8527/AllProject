import configparser
config = configparser.ConfigParser()

def writeConf():
    """写入配置文件"""
    config['mysql'] = {
        'host': '127.0.0.1',
        'port': '3306',
        'user': 'root',
        'password': '123456'
    }
    config['hive'] = {
        'host': '192.168.0.1',
        'port': '27017',
        'user': 'root',
        'password': '123456'
    }
    with open('config.ini', 'a+', encoding='utf-8') as f:
        config.write(f)

def activeConf():
    """操作config 配置文件中所有的配置都是字符串类型"""
    # 得到配置文件里面的数据
    config.read('config.ini', encoding='utf-8')
    # 查看config配置文件中的配置项(配置模块的名字)
    print(config.sections())  # ['mysql', 'hive']
    # 判断mysql是否在config配置中
    print('mysql' in config) # True
    print('hive' in config) # True
    print('hbase' in config) # False

    # 取值
    mysql_host = config['mysql']['host']
    print('mysql_host= ', mysql_host) # mysql_host=  127.0.0.1

    # 循环读值
    for key, values in config['hive'].items():
        print(key, values)
        '''
        host 192.168.0.1
        port 27017
        user root
        password 123456
        '''
    # 找到mysql下所有的键
    print(config.options('mysql'))  #['host', 'port', 'user', 'password']

    # 找到hive下所有的键
    print(config.options('hive'))  #['host', 'port', 'user', 'password']

    # 找到mysql下所有键值对
    print(config.items('mysql')) # [('host', '127.0.0.1'), ('port', '3306'), ('user', 'root'), ('password', '123456')]

    # 找到hive下所有键值对
    print(config.items('hive')) # [('host', '192.168.0.1'), ('port', '27017'), ('user', 'root'), ('password', '123456')]

    # 获取 mysql 下 的 host 的值
    print(config.get('mysql', 'host')) # 127.0.0.1
    # 另一种获取方式
    print(config['mysql'].getint('port')) # port =  3306

    # getint 将得到值转成 int 类型
    port = config.getint('mysql', 'port')
    print('port= ', port, type(port)) # port=  3306 <class 'int'>
    # 同上
    port = config.getfloat('mysql', 'port')
    print('port= ', port, type(port)) # port=  3306.0 <class 'float'>

    # 还有一个getboolean: config.getboolean()
    #getboolean方法可以识别 'yes'/'no', 'on'/'off', 'true'/'false' and '1'/'0'等数据并转换为布尔值

def addConfig():
    # 可以在config.ini配置文件中手动添加配置
    # 添加了中文就需要设置编码格式

    # 手动添加的
    '''
    [tan]
    name = '小明'
    age = '男'
    sex = 23
    '''
    # config.read('config.ini', encoding='utf-8')
    config.read('config.ini')
    # 增加一个配置项
    config.add_section('yuan')
    # 给这个配置项赋值
    config.set('yuan', 'k2', '22222')
    f = open('config.ini', "w")
    config.write(f) # 写进文件
    f.close()
    '''
    [yuan]
    k2 = 22222
    '''


def updateConfig():
    """修改配置"""
    config.read('config.ini')

    # 修改yuan下面的配置项
    config.set('yuan', 'k1', 'a1111')
    config.set('yuan', 'k2', 'b2222')
    config.set('yuan', 'k3', 'c3333')
    config.set('yuan', 'k4', 'd4444')
    '''
    [yuan]
    k2 = b2222
    k1 = a1111
    k3 = c3333
    k4 = d4444
    '''
    f = open('config.ini', "w")
    config.write(f)  # 写进文件
    f.close()

def removeConfig():
    """删除配置"""
    config.read('config.ini')
    # 删除掉 yuan 下的 k1 配置
    config.remove_option('yuan', 'k1')

    # 删除一个section, 将yuan整个配置都给删掉
    config.remove_section('yuan')

    f = open('config.ini', "w")
    config.write(f)  # 写进文件
    f.close()

def main():
    # writeConf()
    # activeConf()
    # addConfig()
    # updateConfig()
    removeConfig()

if __name__ == '__main__':
    main()