from __future__ import annotations

from typing import Union, Any

from util import frozendataclass


@frozendataclass
class Num:
    val: float

    def __repr__(self) -> str:
        return str(self.val)

    def evaluate(self) -> float:
        return self.val

    __float__ = evaluate


@frozendataclass
class Expr:
    a: AST
    b: AST
    op: Any

    def __repr__(self) -> str:
        return f"({self.a} {self.op} {self.b})"

    def evaluate(self) -> float:
        return self.op.func(self.a.evaluate(), self.b.evaluate())

    __float__ = evaluate


AST = Union[Num, Expr]
