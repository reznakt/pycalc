from string import digits as DIGITS, whitespace as WHITESPACE
from typing import List, Optional

from exceptions import TokenizingError
from tokens import Token, NUM, CONSTANTS

FLOAT_SEP = "."
FLOATABLE = DIGITS + FLOAT_SEP


class Lexer:
    def __init__(self, text: str) -> None:
        self.text = text
        self.len = len(text)

        self.char: Optional[str] = None
        self.pos = -1

        self.advance()

    def advance(self) -> None:
        try:
            self.char = self.text[self.pos + 1]
            self.pos += 1
        except IndexError:
            self.char = None

    def tokenize(self) -> List[Token]:
        tokens: List[Token] = []

        while self.char is not None:
            t: Optional[Token] = None

            if self.char in FLOATABLE:
                t = Token(NUM, self._getnum())

            elif self.char in {tt.op.repr for tt in CONSTANTS}:
                try:
                    t = Token(
                        next(tt for tt in CONSTANTS
                             if tt.op is not None and tt.op.repr == self.char))
                    self.advance()
                except ValueError:
                    t = None

            elif self.char in WHITESPACE:
                self.advance()
                continue

            if t is None:
                raise TokenizingError(
                    f"Illegal token {repr(self.char)} at position {self.pos}")

            tokens.append(t)

        return tokens

    def _getnum(self) -> float:
        num = ""

        while self.char is not None and self.char in FLOATABLE:
            num += self.char
            self.advance()

        if num.count(FLOAT_SEP) > 1 or num == FLOAT_SEP:
            raise TokenizingError(
                f"Error while scanning {NUM} token at position {self.pos}")

        return float(num)


def tokenize(text: str) -> List[Token]:
    return Lexer(text).tokenize()
