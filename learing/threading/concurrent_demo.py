from concurrent.futures import ThreadPoolExecutor, as_completed
import requests
from lxml import etree


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
            return temp_dict
    else:
        print('错误响应码为：' + str(response.status_code))


def main():
    """
    concurrent多线程
    :return:
    """
    url = 'https://digital.ucd.ie/index.php?q=&start={}&rows=10'
    works = [url.format(_) for _ in range(1,100)]
    pool = ThreadPoolExecutor(max_workers=10)  # 设置最大的线程数为10

    # 方法一:  用list将任务包裹起来，使用as_completed进行迭代
    jobs = []
    for work in works:
        p = pool.submit(request, work)  # 异步提交任务
        jobs.append(p)
    for _ in as_completed(jobs): # 当某一个future任务执行完毕后，执行下面代码。会阻塞，等待线程完成后执行
        print(_.result())

    # 方法二
    # for work in works:
    #     p = pool.submit(request, work)  # 异步提交任务
    #     p.add_done_callback(lambda x: print(x.result()))

    #方法三:
    # data = pool.map(request, works)  # 取代for循环submit的操作
    # for _ in data:
    #     print(_)


if __name__ == '__main__':
    main()
