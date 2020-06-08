# warnings模块说明
import warnings

a, b = 1, 23

class Twarnings(Warning):
    pass
try:
    assert a == 2
except Exception as e:
    warnings.warn('wrong!', Twarnings)
