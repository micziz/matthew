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
        filename = "save.txt"
        if stext:
            with open("save.txt", "at") as f:
                f.write(f"\n{value}")
            click.echo(f"Saved in {filename}")
        else:
            click.echo(value)
        with open("operations.txt", "at") as f:
            f.write(f"\n{operation}") 
    except Exception as e:
        click.echo(e)
        
if __name__ == '__main__':
    operate()
        