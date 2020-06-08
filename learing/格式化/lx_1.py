def test1():
    name = 'abc'
    print(f'name={name.upper()}')
    dict1 = {'name': 'qer', 'age': 123}
    print(f'名字：{dict1.get("name")},年龄：{dict1.get(str("age"))}')

def main():
    my_dict = {
        'a': 1,
        'b': 2,
        'c': 3
    }
    for k, v in my_dict.items():
        key = f'{k} + {v}'
        print(key)

if __name__ == '__main__':
    test1()
    main()
