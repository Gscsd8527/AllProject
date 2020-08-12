import random


class IteratorSplit:
    def __init__(self, iterator, nums, is_shuffle=False):
        """
        :param iterator: 要拆分的数据，要是可迭代的，比如列表、元组
        :param nums: 可迭代的数据拆分成的 小列表或小元组的长度
        :param is_shuffle: 是否打乱顺序
        """
        self.iterator = iterator
        self.nums = nums
        self.is_shuffle = is_shuffle


    def _split_list(self):
        datas = []
        if self.is_shuffle:
            random.shuffle(self.iterator)
        length = len(self.iterator)
        cs = length // self.nums  #  除数
        sy = length % self.nums  # 余数
        if sy > 0:
            cs += 1
        for i in range(cs):
            temp_list = self.iterator[i * self.nums: (i + 1) * self.nums]
            datas.append(temp_list)
        return datas



def main():
    """
    传入一个列表， 根据给定的值将列表拆分
    """
    a = list(range(100))
    datas = IteratorSplit(a, 15)._split_list()
    for dt in datas:
        print(dt)


if __name__ == '__main__':
    main()