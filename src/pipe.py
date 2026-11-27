from contextlib import contextmanager
from io import StringIO
from subprocess import Popen, PIPE, run
from typing import Generator, IO, Optional, NamedTuple, Union

from cons_list import Cons


def cmd_exec(cmd: str, encoding: str = 'utf-8') -> str:
    return run(cmd, encoding=encoding, shell=True, capture_output=True).stdout


class CommandArgs(NamedTuple):
    cmd: Union[str, list[str]]
    encoding: str = 'cp932'
    shell: bool = False


class ShellCommand(Cons[CommandArgs]):

    @classmethod
    def of(cls, cmd: Union[str, list[str]], encoding: str = 'cp932', shell: bool = False, tail: Optional['ShellCommand'] = None) -> 'ShellCommand':
        return cls(CommandArgs(cmd, encoding, shell), tail)

    def __or__(self, other: 'ShellCommand') -> 'ShellCommand':
        return self. __add__(other)

    def capture_output(self, reader: Optional[IO[str]] = None) -> str:
        with self.cmd_open(reader) as reader2:
            return self.tail.capture_output(reader2) if self.tail else reader2.read()

    def read_output(self, reader: Optional[IO[str]] = None) -> Generator[str, None, None]:
        with self.cmd_open(reader) as reader2:
            if self.tail is None:
                yield from reader2
            else:
                with self.tail.read_output(reader2) as reader3:
                    yield from reader3

    @contextmanager
    def cmd_open(self, upstream: Optional[IO[str]] = None) -> Generator[IO[str], None, None]:
        with Popen(self.value.cmd, shell=True, encoding=self.value.encoding, stdout=PIPE, stdin=None if upstream is None else PIPE) as proc:
            if proc is None:
                return

            if upstream:
                with proc.stdin as writer:
                    for line in proc.stdin:
                        writer.write(line)

            with proc.stdout or StringIO() as downstream:
                yield downstream


if __name__ == '__main__':
    dir_command = ShellCommand(CommandArgs('dir'))
    for line in dir_command.read_output():
        print(line, end='')
