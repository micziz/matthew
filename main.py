from email.policy import default
import click
from src._parser_ import Parser
from src.interpreter import Interpreter
from src.lexer import Lexer


@click.command()
@click.option('--operation', prompt='Operation',
              help='Operation To interpret.')
@click.option('--stext', is_flag=True, help="Save operation to text")
def operate(operation, stext):
    try:
        text = operation
        lexer = Lexer(text)
        tokens = lexer.generate_tokens()
        parser = Parser(tokens)
        tree = parser.parse()
        interpreter = Interpreter()
        value = interpreter.visit(tree)
        if stext:
            with open("save.txt", "at") as f:
                f.write(f"\n{value}")
        else:
            click.echo(value)
    except Exception as e:
        click.echo(e)
        
if __name__ == '__main__':
    operate()
        