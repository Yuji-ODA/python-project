from threading import Timer, Thread
from typing import Callable, Optional


def scheduler(proc: Callable[[], None], delay: int, limit: Optional[int], count: int = 0):
    if limit is not None and limit < count:
        return
    Timer(delay, lambda: scheduler(proc, delay, limit, count + 1)).start()
    0 < count and proc()


def schedule(proc: Callable[[], None], delay: int, limit: Optional[int] = None) -> Thread:
    return Thread(target=scheduler(proc, delay, limit))


if __name__ == '__main__':
    from datetime import datetime

    schedule(lambda: print(datetime.now()), 1, 10).start()
