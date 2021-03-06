# This is the parser file, containing the parser. The reason that the files name is _parser_ is to avoid conflicts
# With a python inbuilt function. The parser gets the tokens generated by the lexer and generates an AST (abstract syntax tree) from that
# All code inside this file, unless otherwise noted, is licensed under Apache 2.0 License.

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

    # Expression method
    def expr(self):
        # Call a term and set it to result
        result = self.term()

        # While the current token is not not none
        # and the current token is either plus or minus
        while self.current_token != None and self.current_token.type in (
            TokenType.PLUS,
            TokenType.MINUS,
        ):
            # If the current token is plus
            if self.current_token.type == TokenType.PLUS:
                # Advance
                self.advance()
                # Return a SddNode and assign it to result.
                # Also, we pass result, and a term
                result = AddNode(result, self.term())
            # Else the token type is minus
            elif self.current_token.type == TokenType.MINUS:
                # Advance
                self.advance()
                # Return a SubtractNode and assign it to result.
                # Also, we pass result, and a term
                result = SubtractNode(result, self.term())

        # Return result
        return result

    # Term method
    def term(self):
        # Result is factor method
        result = self.factor()

        # While the current token is not not none
        # and the current token is either multply or divide
        while self.current_token != None and self.current_token.type in (
            TokenType.MULTIPLY,
            TokenType.DIVIDE,
        ):
            # If it's multiply
            if self.current_token.type == TokenType.MULTIPLY:
                # Advance
                self.advance()
                # Return a MultiplyNode and assign it to result.
                # Also, we pass result, and a factor
                result = MultiplyNode(result, self.factor())
            # If it's divide
            elif self.current_token.type == TokenType.DIVIDE:
                # Advance
                self.advance()
                # Return a DivideNode and assign it to result.
                # Also, we pass result, and a factor
                result = DivideNode(result, self.factor())

        # Return result
        return result

    # Factor Method
    def factor(self):
        # Assign tokens
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
