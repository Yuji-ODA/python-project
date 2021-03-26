
from subprocess import Popen, PIPE
from operator import methodcaller
from contextlib import contextmanager


@contextmanager
def pipe_exec(cmd: str, encoding='utf-8'):
    with Popen(cmd, shell=True, stdout=PIPE) as proc:
        yield map(methodcaller('decode', encoding), proc.stdout)
