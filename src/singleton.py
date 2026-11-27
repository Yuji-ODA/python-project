from collections import namedtuple


class Singleton(type):
    __INSTANCES = {}

    InstanceKey = namedtuple('InstanceKey', 'cls args kwargs')

    def __new__(cls, name, bases, class_dict, *args):
        print((cls, name, bases, class_dict, args))
        return super().__new__(cls, name, bases, class_dict)

    def __call__(cls, *args, **kwargs):
        print((cls, args, kwargs))
        instance_key = cls.InstanceKey(cls, args, frozenset(kwargs.items()))
        if instance_key not in cls.__INSTANCES:
            cls.__INSTANCES[instance_key] = super().__call__(*args, **kwargs)
        print(cls.__INSTANCES)
        return cls.__INSTANCES[instance_key]


if __name__ == '__main__':
    class CS(metaclass=Singleton):
        @classmethod
        def hoge(cls):
            return cls.__INSTANCES['hoge']

        def __init__(self):
            self.__a = 1
            self._b = 1

    print(id(CS()))
    print(id(CS()))

    class CF(metaclass=Singleton):
        def __init__(self, a, b='おいら'):
            self.__a, self.__b = a, b

        @property
        def a(self):
            return self.__a

    print(CF('俺').a)
    print(CF(a='俺').a)
    print(id(CF(a='そなた', b='わてら')))
    print(id(CF(a='そなた', b='わてら')))
    print(CF('お前').a)
