class _const(object):  # 自定义一个常量类
    """自定义常量类"""

    class ConstError(BaseException):
        pass  # 内部自定义修改常量值异常

    class ConstCaseError(ConstError):
        pass  # 内部自定义常量非大写异常

    def __setattr__(self, name, value):  # setattr 魔法方法在类属性赋值时 自动调用 可实现我们抛出异常的操作
        """
        name和value 在进行赋值操作，会自动传入
        name: 常量名
        value： 常量值
        """
        if name in self.__dict__.keys():  # 判断 常量名是否存在 存在抛出异常
            raise self.ConstError("constant reassignment error!")
        if not name.isupper():  # 判断 常量名是否全为大写 非全部大写抛出异常
            raise self.ConstCaseError("const name '%s' is not all uppercase " % name)
        self.__dict__[name] = value  # 满足上述条件 进行赋值操作

import sys

sys.modules[__name__] = _const()  # 为方便模块导入 将类名绑定到本模块名上 ，导入后可直接使用 模块名 const.PI 来操作常量