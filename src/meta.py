import logging


class Meta(type):
    def __new__(meta, name, bases, class_dict):
        print('Meta.__new__: ', meta, name, bases, class_dict)
        cls = super().__new__(meta, name, bases, class_dict)
        print(cls)
        cls.logger = logging.getLogger(cls.__qualname__)
        return cls

    def __call__(cls, *args, **kwargs):
        print('Mate.__call__: ', cls, args, kwargs)
        instance = super().__call__(*args, **kwargs)
        print('Meta.__call__: instance created: ' + instance.__repr__())
        return instance


class MyClass(metaclass=Meta):
    def __new__(cls, *args):
        print('MyClass.__new__: ', super(), cls, args)
        instance = super().__new__(cls)
        print('MyClass.__new__: instance created: ' + instance.__repr__())
        return instance

    def __init__(self, x):
        self.x = x


class MySubClass(MyClass):
    def __new__(cls, *args):
        print('MySubClass.__new__: ', super(), cls, args)
        cls.injected = 'OK!!'
        instance = super().__new__(cls)
        print('MySubClass.__new__: instance created: ' + instance.__repr__())
        return instance

    def __init__(self, x, y):
        super().__init__(x)
        self.y = y


p=MyClass(10)
print(p.x, p.logger)

c=MySubClass('gaggag', 'hogehoge')
print(c.x, c.y, c.logger)
