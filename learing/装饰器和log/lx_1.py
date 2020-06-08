import functools
import datetime, time

def log_time(func):
    @functools.wraps(func)
    def get_time(*args, **kwargs):
        start = time.time()
        res = func(*args, **kwargs)
        end = time.time()
        now = datetime.datetime.today()
        data_json = {
            'start': start,
            'end': end,
            'now': now
        }
        print(data_json)
        return res
    return get_time

@log_time
def a1():
    print('a1')

@log_time
def a2():
    print('a2')

def main():
    a1()
    a2()

if __name__ == '__main__':
    main()