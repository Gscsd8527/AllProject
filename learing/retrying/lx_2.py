from retry import retry

@retry()
def mytest1():
    '''
    Retry until succeed'
    重试，直至成功
    '''


@retry(ZeroDivisionError, tries=3, delay=2)
def mytest2():
    '''
    Retry on ZeroDivisionError, raise error after 3 attempts, sleep 2 seconds between attempts.
    重试ZeroDivisionError, 3次尝试后引发错误，两次尝试之间休眠2秒。
    '''
    print('aaa')
    a = 1/0


@retry((ValueError, TypeError), delay=1, backoff=2)
def mytest3():
    '''
    Retry on ValueError or TypeError, sleep 1, 2, 4, 8, ... seconds between attempts.
   重试ValueError或TypeError, sleep 1, 2, 4, 8，…秒之间。
    '''

@retry((ValueError, TypeError), delay=1, backoff=2, max_delay=4)
def mytest4():
    '''
    Retry on ValueError or TypeError, sleep 1, 2, 4, 4, ... seconds between attempts.
   重试ValueError或TypeError, sleep 1, 2, 4, 4，…秒之间。
    '''

@retry(ValueError, delay=1, jitter=1)
def mytest5():
    '''
    Retry on ValueError, sleep 1, 2, 3, 4, ... seconds between attempts.
   重试ValueError, sleep 1, 2, 3, 4，…秒之间
    '''


def main():
    mytest1()
    mytest2()

if __name__ == '__main__':
    main()