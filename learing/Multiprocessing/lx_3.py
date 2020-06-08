from multiprocessing import Process
import time
def worker(str1):
    print('worker start')
    time.sleep(2)
    print('-------', str1)
    print('worker end')

if __name__ == '__main__':
    start_time = time.time()
    print('父进程启动')
    process_list = []
    for i in range(3):
        process = Process(target=worker, args=(i,))
        process_list.append(process)
    for process in process_list:
        process.start()
    for process in process_list:
        process.join()
    print('父进程结束')
    print('耗时： ', time.time() - start_time)
