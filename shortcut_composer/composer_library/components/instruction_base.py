from typing import List
from dataclasses import dataclass


class Instruction:
    def enter(self) -> 'Instruction': return self
    def update(self) -> None: ...
    def exit(self, *_) -> None: ...
    def __enter__(self) -> 'Instruction': return self.enter()
    def __exit__(self, *_) -> None: self.exit()


@dataclass
class InstructionHolder:
    __instructions: List[Instruction]

    def enter(self) -> 'InstructionHolder':
        for instruction in self.__instructions:
            instruction.enter()
        return self

    def update(self) -> None:
        for instruction in self.__instructions:
            instruction.update()

    def exit(self, *_) -> None:
        for instruction in self.__instructions:
            instruction.exit()

    def __enter__(self) -> 'InstructionHolder':
        return self.enter()

    def __exit__(self, *_) -> None:
        self.exit()
