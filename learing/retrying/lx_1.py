from retrying import retry
import random

def jieshao():
    """
    retrying 是一个 python 的重试包，可以用来自动重试一些可能运行失败的程序段
    retrying提供一个装饰器函数retry，被装饰的函数就会在运行失败的条件下重新执行，默认只要一直报错就会不断重试。

    参数：
    stop_max_attempt_number：  用来设定最大的尝试次数，超过该次数就停止重试
    stop_max_delay：比如设置成10000，那么从被装饰的函数开始执行的时间点开始，
                    到函数成功运行结束或者失败报错中止的时间点，只要这段时间超过10秒，函数就不会再执行了

    wait_fixed：设置在两次retrying之间的停留时间

    wait_random_min和wait_random_max：用随机的方式产生两次retrying之间的停留时间

    wait_exponential_multiplier和wait_exponential_max：以指数的形式产生两次retrying之间的停留时间，
         产生的值为2^previous_attempt_number * wait_exponential_multiplier，previous_attempt_number是前面已经retry的次数，
        如果产生的这个值超过了wait_exponential_max的大小，那么之后两个retrying之间的停留值都为wait_exponential_max。
        这个设计迎合了exponential backoff算法，可以减轻阻塞的情况。
    :return:
    """
@retry
def mytest1():
    if random.randint(0, 10) > 1:
        raise IOError("Broken sauce, everything is hosed!!!111one")
    else:
        return "Awesome sauce!"

a = 1
@retry()
def mytest2():
    b = 100
    global a
    if a < b:
        # print('a= ', a)
        a += 1
        raise ImportError('小于 b')
    else:
        print('大于或等于 b')
        return a



def main():
    print(mytest1())
    print('a 的值为： ', mytest2())

if __name__ == '__main__':
    main()