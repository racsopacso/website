from more_itertools import peekable
from typing import Iterator, List, Tuple

class InterpretedArgsIterable:
    def __init__(self, *args):
        self.iterator = peekable(args)
        self.flags_and_flag_args = {}

        for arg in self.iterator:
            if arg.startswith("--"):
                flag_body = arg[2:]

                self.add_more_args(flag_body)

                continue

            if arg.startswith("-"):
                if len(arg) == 2:
                    self.add_more_args(arg[1])

                else:
                    try:
                        peek = self.iterator.peek()

                    except StopIteration:
                        peek = None

                    if peek and not peek.startswith("-"):
                        raise ValueError("Arguments after combined flag: " + arg + " " + peek)

                    self.flags_and_flag_args.update({char:[] for char in arg[1:]})
            else:
                raise ValueError("Argument without flag: " + arg)

    def __iter__(self) -> Iterator[Tuple[str, List[str]]]:
        return iter(self.flags_and_flag_args.items())

    def __repr__(self):
        return "Interpreted args: " + str(self.flags_and_flag_args)

    def add_more_args(self, flag_body):
        flag_args = []

        while True:
            try:
                peek = self.iterator.peek()
            except StopIteration:
                break

            if peek.startswith("-"):
                break

            else:
                flag_args.append(next(self.iterator))

        self.flags_and_flag_args[flag_body] = self.flags_and_flag_args.get(flag_body, []) + flag_args






