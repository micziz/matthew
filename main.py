# This is the main file, containing the CLI, and the functions needed to lex, parse and interpret
# the operation. All code inside this file, unless otherwise noted, is licensed under the Apache-2.0 License


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
# whether to save to operations.txt (default yes)
@click.option('--nosave', is_flag=True, help="Don't save in operations.py")
# Operate function.
def operate(operation, stext, nosave):
    # Try except for errors
    try:
        # Operation is what is passed in --operation (if not passed it will be prompted)
        text = operation
        # Initialize the lexer class, with text passed as parameters
        lexer = Lexer(text)
        # Generate all tokens
        tokens = lexer.generate_tokens()
        # Initialize the parser class, with tokens passed as parameters
        parser = Parser(tokens)
        # Generate a tree
        tree = parser.parse()
        # Initialize the interpreter class
        interpreter = Interpreter()
        # Interpret the tree and send it to value
        value = interpreter.visit(tree)
        # Filename, needed for later
        filename = "save.txt"
        # If the --stext (save text) option is passed:
        if stext:
            # Open save.txt
            with open(filename, "at") as f:
                # Save the result of the operation
                f.write(f"\n{value}")
            # Print that it has been saved.
            click.echo(f"Saved in {filename}")
        # Else, simply print the result
        else:
            click.echo(value)
        # If the option --nosave is not passed
        if not nosave:
            # Then open operations.txt
            with open("operations.txt", "at") as f:
                # and save the just inputted operation
                f.write(f"\n{operation}") 
        # Else
        else:
            # Print that it is not going to save to operations.txt
            click.echo("Will not save the operation in operations.txt")
    # Except is for catching errors
    except Exception as e:
        # Print error
        click.echo(e)
    
# Run the main Function
if __name__ == '__main__':
    operate()
        