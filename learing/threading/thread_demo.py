import requests
from lxml import etree
import threading


THREAD_NUM = 10  # 启动十个线程


def request(url):
    """
    发起请求
    :param url: 需要请求的url
    :return:
    """
    response = requests.get(url)
    if response.status_code == 200:
        text = response.text
        html_xpath = etree.HTML(text)
        rows = html_xpath.xpath('//div[@class="row results-row"]/div')
        for row in rows:
            title = row.xpath('.//h4/a/text()')[0]
            url = row.xpath('.//img/@src')[0]
            temp_dict = {
                'title': title,
                'url': url,
            }
            print(temp_dict)
    else:
        print('错误响应码为：' + str(response.status_code))


def start_thread(works):
    """
    开启多线程
    :param works: 需要抓取的url列表
    :return:
    """
    nums = len(works)
    x = nums // THREAD_NUM
    ys = nums % THREAD_NUM
    if ys > 0:
        x += 1
    for i in range(x):
        print('循环第  {}   次， 共有   {}   次'.format(i, x))
        if i == x + 1:
            work = works[i * THREAD_NUM:]
        else:
            work = works[i * THREAD_NUM:(i + 1) * THREAD_NUM]
        threads = [threading.Thread(target=request(job), args=(job,)) for job in work]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()


def main():
    """
    threading多线程
    :return:
    """
    url = 'https://digital.ucd.ie/index.php?q=&start={}&rows=10'
    works = [url.format(_) for _ in range(1,100)]
    start_thread(works)


if __name__ == '__main__':
    main()
