# This is the parser file, containing the parser. The reason that the files name is _parser_ is to avoid conflicts
# With a python inbuilt function. All code inside this, unless otherwise noted, is licensed under Apache 2.0 License.

# Imports
from src.tokens import TokenType
from src.nodes import *

# Start of the parser class
class Parser:

    # Constructor
    def __init__(self, tokens):
        # Start an iteration of tokens
        self.tokens = iter(tokens)
        # Advance to the next token (in this case to the first token)
        self.advance()

    # Raise error method
    def raise_error(self, e):
        # Raise a invalid exception.
        raise Exception(
            f"""
    Invalid Syntax Error
    {e}
"""
        )

    # Advance method
    def advance(self):
        # Try
        try:
            # Advance using the next() by python
            self.current_token = next(self.tokens)
        # Except the iteration ended
        except StopIteration:
            # Assign the current token to none
            self.current_token = None

    # Parse method (entry point for the parser)
    def parse(self):
        # If the current token is none
        if self.current_token == None:
            # Return none
            return None

        # Run the expression method and assign it to result
        result = self.expr()

        # If the current token is not none
        if self.current_token != None:
            # Raise an error
            self.raise_error("Token Not none!")

        # Return result
        return result

    # Expr
    def expr(self):
        result = self.term()

        while self.current_token != None and self.current_token.type in (
            TokenType.PLUS,
            TokenType.MINUS,
        ):
            if self.current_token.type == TokenType.PLUS:
                self.advance()
                result = AddNode(result, self.term())
            elif self.current_token.type == TokenType.MINUS:
                self.advance()
                result = SubtractNode(result, self.term())

        return result

    def term(self):
        result = self.factor()

        while self.current_token != None and self.current_token.type in (
            TokenType.MULTIPLY,
            TokenType.DIVIDE,
        ):
            if self.current_token.type == TokenType.MULTIPLY:
                self.advance()
                result = MultiplyNode(result, self.factor())
            elif self.current_token.type == TokenType.DIVIDE:
                self.advance()
                result = DivideNode(result, self.factor())

        return result

    def factor(self):
        token = self.current_token

        if token.type == TokenType.LPAREN:
            self.advance()
            result = self.expr()

            if self.current_token.type != TokenType.RPAREN:
                self.raise_error(f"Expected RPAREN found {token}")

            self.advance()
            return result

        elif token.type == TokenType.NUMBER:
            self.advance()
            return NumberNode(token.value)
        elif token.type == TokenType.PLUS:
            self.advance()
            return PlusNode(self.factor())

        elif token.type == TokenType.MINUS:
            self.advance()
            return MinusNode(self.factor())

        self.raise_error(f"Expected Term, found {token}")
