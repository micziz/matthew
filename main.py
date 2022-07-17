import click
from src._parser_ import Parser
from src.interpreter import Interpreter
from src.lexer import Lexer


@click.command()
@click.option('--operation', prompt='Operation',
              help='Operation To interpret.')
def operate(operation):
    try:
        text = operation
        lexer = Lexer(text)
        tokens = lexer.generate_tokens()
        parser = Parser(tokens)
        tree = parser.parse()
        interpreter = Interpreter()
        value = interpreter.visit(tree)
        click.echo(value)
    except Exception as e:
        click.echo(e)
        
if __name__ == '__main__':
    operate()
        