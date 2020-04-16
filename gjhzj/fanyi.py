import http.client
import hashlib
import urllib
import random
import json
import pandas as pd

class FANYI:
    """"
    将英文名机构装换成中文名机构
    """
    def __init__(self):
        self.inst_set = self.getYzqInit()

    def _RUN1(self):
        """
        启动函数，执行第一种方法，单个翻译
        :param keyword:
        :return:
        """
        inst_list = self.getEnglistInstName1()
        for keyword in inst_list:
            if keyword not in self.inst_set:
                result = self.baidu(keyword)
                if result:
                    print(result)
                    try:
                        """
                        避免出现请求过快，数据报错
                        """
                        chinese = result['trans_result'][0]['dst']
                        print(chinese)
                        data_json = {
                            'englist': keyword,
                            'chinese': chinese,
                        }
                        data_str = json.dumps(data_json, ensure_ascii=False)
                        with open('data.json', 'a+', encoding='utf-8') as f:
                            f.write('{}\n'.format(data_str))

                        # 将已抓取的放到文件里面去
                        with open('yzq.txt', 'a+', encoding='utf-8') as f:
                            f.write('{}\n'.format(keyword))
                    except:
                        pass

                    import time
                    time.sleep(1)

            else:
                print('已抓取')


    def _RUN2(self):
        """
        执行第二种方法，多个英文机构名称一块拆
        :param keyword:
        :return:
        """
        inst_list = self.getEnglistInstName2()
        for inst_lst in inst_list:
            inst_str = ' + '.join(inst_lst)
            if inst_str not in self.inst_set:
                result = self.baidu(inst_str)
                if result:
                    print(result)
                    chinese = result['trans_result'][0]['dst']
                    print(chinese)
                    chinese_list = chinese.split('+')
                    eng_china_zip = zip(inst_lst, chinese_list)
                    for inst in eng_china_zip:
                        data_json = {
                            'englist': inst[0],
                            'chinese': inst[1],
                        }
                        data_str = json.dumps(data_json, ensure_ascii=False)
                        with open('data.json', 'a+', encoding='utf-8') as f:
                            f.write('{}\n'.format(data_str))

                    # 将已抓取的放到文件里面去
                    with open('yzq.txt', 'a+', encoding='utf-8') as f:
                        f.write('{}\n'.format(inst_str))

                    import time
                    time.sleep(1)
            else:
                print('数据已抓取过')

    @staticmethod
    def baidu(keyword):
        # 百度通用翻译API,不包含词典

        appid = '20200415000420719'  # 填写你的appid
        secretKey = 'udsMVSTjJHrD4Tb7Ntkc'  # 填写你的密钥

        httpClient = None
        myurl = '/api/trans/vip/translate'

        fromLang = 'auto'  # 原文语种
        toLang = 'zh'  # 译文语种
        salt = random.randint(32768, 65536)  # 随机数
        q = keyword
        sign = appid + q + str(salt) + secretKey
        sign = hashlib.md5(sign.encode()).hexdigest()
        myurl = myurl + '?appid=' + appid + '&q=' + urllib.parse.quote(
            q) + '&from=' + fromLang + '&to=' + toLang + '&salt=' + str(
            salt) + '&sign=' + sign

        try:
            httpClient = http.client.HTTPConnection('api.fanyi.baidu.com')
            httpClient.request('GET', myurl)

            # response是HTTPResponse对象
            response = httpClient.getresponse()
            result_all = response.read().decode("utf-8")
            result = json.loads(result_all)

            return result

        except Exception as e:
            print('e= ', e)
        finally:
            if httpClient:
                httpClient.close()

    @staticmethod
    def youdao(keyword):
        """
        有道翻译
        :param keyword:
        :return:
        """
        pass

    @staticmethod
    def getEnglistInstName1():
        """
        获取机构名
        :return:
        """
        df = pd.read_excel('inst.xlsx')
        inst_list = df['机构英文名称'].tolist()
        return inst_list

    @staticmethod
    def getEnglistInstName2():
        """
        获取机构名，将机构多个多个的组合在一起
        :return:
        """
        df = pd.read_excel('inst.xlsx')
        inst_list = df['机构英文名称'].tolist()
        # 拆分inst列表
        NUM = 5  # 机构拼接个数
        nums = len(inst_list)
        inst_list_new = []
        x = nums // NUM
        xs = x + 2
        for i in range(xs):
            if i == x + 1:
                lst = inst_list[i * NUM:]
            else:
                lst = inst_list[i * NUM:(i + 1) * NUM]
            inst_list_new.append(lst)

        return inst_list_new

    @staticmethod
    def getYzqInit():
        """
        获取已抓取的机构
        :return:
        """
        try:
            f = open('yzq.txt', 'r', encoding='utf-8')
            data = f.readlines()
            data_list = [dt.strip('\n') for dt in data]
            f.close()
        except:
            # 如果文件不存在就创建一个文件， 如果文件存在就打开，不存在就创建
            f = open("yzq.txt", 'w')
            f.close()
            data_list = []
        return data_list

def main():
    fanyi = FANYI()
    fanyi._RUN1()

if __name__ == '__main__':
    main()
