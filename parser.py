from typing import List
from typing import Optional

from ast import AST, Expr, Num
from exceptions import ParsingError, EmptyExpressionError
from tokens import Token, ADD, SUB, MUL, DIV, MOD, POW, LPAR, RPAR, NUM


class Parser:
    def __init__(self, tokens: List[Token]) -> None:
        self.tokens = iter(tokens)
        self.token: Optional[Token] = None

        self.advance()

    def advance(self) -> None:
        self.token = next(self.tokens, None)

    def parse(self) -> AST:
        if self.token is None:
            raise EmptyExpressionError(
                "Cannot parse an empty sequence of tokens")

        result = self._getexpr()

        if self.token is not None:
            raise ParsingError(f"Error while parsing token {self.token}")

        return result

    def _getexpr(self) -> AST:
        result: AST = self._getterm()

        while self.token is not None and self.token.type in (ADD, SUB):
            token = self.token
            self.advance()
            result = Expr(result, self._getterm(), token.type.op)

        return result

    def _getterm(self) -> AST:
        result: AST = self._getimmediate()

        while self.token is not None and self.token.type in (MUL, DIV):
            token = self.token
            self.advance()
            result = Expr(result, self._getimmediate(), token.type.op)

        return result

    def _getimmediate(self) -> AST:
        result: AST = self._getfactor()

        while self.token is not None and self.token.type in (MOD, POW):
            token = self.token
            self.advance()
            result = Expr(result, self._getfactor(), token.type.op)

        return result

    def _getfactor(self) -> AST:
        token = self.token

        if token is None:
            raise ParsingError("Unexpected EOF while parsing number literal")

        if token.type is LPAR:
            self.advance()
            result = self._getexpr()

            if self.token is None or self.token.type is not RPAR:
                raise ParsingError(
                    "Unexpected EOF while parsing parenthesised expression")

            self.advance()
            return result

        elif token.type is NUM:
            self.advance()
            return Num(token.value)

        elif token.type in (ADD, SUB):
            self.advance()
            return Num(
                self._getfactor().val * (-1 if token.type is SUB else 1)
            )

        raise ParsingError(
            f"Unexpected token while parsing number literal: {self.token}")


def parse(tokens: List[Token]) -> Optional[AST]:
    return Parser(tokens).parse()
