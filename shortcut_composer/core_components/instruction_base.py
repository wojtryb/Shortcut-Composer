from typing import List


class Instruction:
    """
    Component that allows to perform additional tasks outside the main logic.

    Depending on the picked instruction, tasks can be performed on key
    press and release.
    """

    def enter(self) -> 'Instruction': return self
    def exit(self, *_) -> None: ...
    def __enter__(self) -> 'Instruction': return self.enter()
    def __exit__(self, *_) -> None: self.exit()


class InstructionHolder:

    def __init__(self, instructions: List[Instruction] = []) -> None:
        self.__instructions = instructions

    def enter(self) -> 'InstructionHolder':
        for instruction in self.__instructions:
            instruction.enter()
        return self

    def exit(self, *_) -> None:
        for instruction in self.__instructions:
            instruction.exit()

    def __enter__(self) -> 'InstructionHolder':
        return self.enter()

    def __exit__(self, *_) -> None:
        self.exit()
