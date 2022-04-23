import time

from exceptions import TokenizingError, ParsingError, EmptyExpressionError
from lexer import tokenize
from parser import parse


def main() -> None:
    while True:
        x = input(">>> ")
        try:
            timer = time.perf_counter()
            tokens = tokenize(x)
            ast = parse(tokens)
            print(
                f"tokens: {tokens}",
                f"AST: {ast}",
                f"result: {ast.evaluate()}",
                f"{(time.perf_counter() - timer) * 1000} ms", sep="\n"
            )
        except (TokenizingError, ParsingError) as e:
            print(str(e))
        except EmptyExpressionError:
            pass


if __name__ == '__main__':
    main()
