import pprint

def main():
    data = (
        "this is a string", [1, 2, 3, 4], ("more tuples",
         1.0, 2.3, 4.5), "this is yet another string"
    )
    print(data)
    pprint.pprint(data)

if __name__ == '__main__':
    main()