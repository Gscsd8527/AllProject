import asyncio
from time import sleep, time

def wirte(i):
    print('i = ', i)
    with open('a.txt', 'a+') as f:
        f.write('{}\n'.format(i))

def miss(i):
    sleep(1)
    wirte(i)

def start():
    for i in range(10):
        miss(i)

def main():
    loop = asyncio.get_event_loop()
    start_time = time()
    start()
    print('总耗时： ', time() - start_time)

if __name__ == '__main__':
    main()