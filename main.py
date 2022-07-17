from src._parser_ import Parser
from src.interpreter import Interpreter
from src.lexer import Lexer

while True:
    try:
        text = input("matthew > ")
        lexer = Lexer(text)
        tokens = lexer.generate_tokens()
        parser = Parser(tokens)
        tree = parser.parse()
        if not tree: continue
        interpreter = Interpreter()
        value = interpreter.visit(tree)
        print(value)
    except Exception as e:
        print(e)
        