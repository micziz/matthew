# Imports
import click
from src._parser_ import Parser
from src.interpreter import Interpreter
from src.lexer import Lexer

# Create a click command
@click.command()
# Option for the prompt
@click.option('--operation', prompt='Operation',
              help='Operation To interpret.')
# whether to save to text
@click.option('--stext', is_flag=True, help="Save operation to text")
@click.option('--nosave', is_flag=True, help="Don't save in operations.py")
def operate(operation, stext, nosave):
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
        if not nosave:
            with open("operations.txt", "at") as f:
                f.write(f"\n{operation}") 
    except Exception as e:
        click.echo(e)
        
if __name__ == '__main__':
    operate()
        