import operator
from typing import Optional, Callable

from util import frozendataclass


@frozendataclass
class Operator:
    repr: str
    func: Optional[Callable[[float, float], float]] = None

    def __repr__(self) -> str:
        return self.repr


@frozendataclass
class TokenType:
    name: str
    op: Optional[Operator] = None

    def __repr__(self) -> str:
        return self.name


@frozendataclass
class Token:
    type: TokenType
    value: Optional[float] = None

    def __repr__(self) -> str:
        return (f"{self.type}"
                + (f": {repr(self.value)}"
                   if self.value is not None else ""))


def tt(
        name: str,
        op: Optional[str] = None,
        func: Optional[Callable[[float, float], float]] = None
) -> TokenType:
    return TokenType(name, (Operator(op, func) if op is not None else None))


NUM = tt("NUM")
LPAR = tt("LPAR", "(")
RPAR = tt("RPAR", ")")
ADD = tt("ADD", "+", operator.add)
SUB = tt("SUB", "-", operator.sub)
MUL = tt("MUL", "*", operator.mul)
DIV = tt("DIV", "/", operator.truediv)
POW = tt("POW", "^", operator.pow)
MOD = tt("MOD", "%", operator.mod)

ALL = {v for _, v in globals().items() if isinstance(v, TokenType)}
CONSTANTS = {tt_ for tt_ in ALL if tt_.op is not None}
