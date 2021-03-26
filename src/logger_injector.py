import logging


def create_logger(name: str, level: int, fmt: str = logging.BASIC_FORMAT):
    logger = logging.getLogger(name)
    logger.setLevel(level)
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter(fmt))
    logger.addHandler(handler)
    return logger


def logger(level: int = logging.WARNING, fmt: str = logging.BASIC_FORMAT):
    def wrapper(cls):
        cls.logger = create_logger(name=cls.__qualname__, level=level, fmt=fmt)
        return cls
    return wrapper


if __name__ == '__main__':
    @logger(level=logging.INFO, fmt='%(asctime)s [%(levelname)s] - %(name)s %(funcName)s: %(message)s')
    class MyClass:
        def f(self, a):
            self.logger.info(a)

    @logger(level=logging.INFO, fmt='%(asctime)s [%(levelname)s] - %(name)s %(funcName)s: %(message)s')
    class ChildClass(MyClass):
        pass

    i = MyClass()
    i.f('hoge')

    ChildClass().f('huga')

    print(MyClass.logger, ChildClass.logger)
