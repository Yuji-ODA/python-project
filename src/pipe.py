
from contextlib import contextmanager
from subprocess import Popen, PIPE
from typing import Iterator


@contextmanager
def pipe_exec(cmd: str, message: str = None, encoding: str = 'utf-8') -> Iterator[str]:
    with Popen(cmd, shell=True, stdout=PIPE, stdin=None if message is None else PIPE) as proc:
        if proc is not None:

            print(message, file=proc.stdin)
            proc.stdin.close()

        for line in proc.stdout:
            yield line.decode(encoding)
