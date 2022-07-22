# This is the main file, containing the CLI, and the functions needed to lex, parse and interpret
# the operation. All code inside this file, unless otherwise noted, is licensed under the Apache-2.0 License


# Imports
import click
from src._parser_ import Parser
from src.interpreter import Interpreter
from src.lexer import Lexer
from sys import exit

# Create a click command
@click.command()
# Option for the prompt
@click.option("--operation", "-O", prompt="Operation", help="Operation To interpret.")
# whether to save to text
@click.option("--stext", "-ST", is_flag=True, help="Save operation to text")
# whether to save to operations.txt (default yes)
@click.option("--nosave", "-NS", is_flag=True, help="Don't save in operations.py")
# whether to generate just the ast
@click.option("--ast", is_flag=True, help="Generate just the Abstract Syntax Tree")
# whether to run just the lexer
@click.option("--jlexer", "-JL", is_flag=True, help="Run just the lexer")
# whether to be verbose
@click.option("--verbose", "-V", is_flag=True, help="Be more verbose")
# whether to be silent
@click.option("--silent", "-S", is_flag=True, help="Be more silent")
# Operate function.
def operate(operation, stext, nosave, ast, jlexer, verbose, silent):
    _version_ = "0.2.0"
    click.echo(f"matthew version {_version_}")
    # Try except for errors
    try:
        # Operation is what is passed in --operation (if not passed it will be prompted)
        text = operation
        if verbose:
            click.echo("Running the lexer")
        if jlexer:
            # Initialize the lexer class, with text passed as parameters
            lexer = Lexer(text)
            # Generate all tokens
            tokens = lexer.generate_tokens()
            if stext:
                if verbose:
                    click.echo("Saving in file")
                # Open save.txt
                with open("save.txt", "at") as f:
                    f.write("\n")
                    for token in tokens:
                        f.write(str(f"{token} "))
            else:
                click.echo(list(tokens))
            click.echo("Saving the input to operations.txt")
            with open("operations.txt", "at") as f:
                f.write(f"\n{operation} (just lexer)")
            exit()
        else:
            lexer = Lexer(text)
            # Generate all tokens
            tokens = lexer.generate_tokens()
        if verbose:
            click.echo("Generating AST")
        # Initialize the parser class, with tokens passed as parameters
        parser = Parser(tokens)
        # Generate a tree
        tree = parser.parse()
        if not ast:
            if verbose:
                click.echo("Interpreting")
            # Initialize the interpreter class
            interpreter = Interpreter()
            # Interpret the tree and send it to value
            value = interpreter.visit(tree)
            # Filename, needed for later
        filename = "save.txt"
        # If the --stext (save text) option is passed:
        if stext:
            if verbose:
                print("Saving in file")
            # Open save.txt
            with open(filename, "at") as f:
                # Save the result of the operation
                if not ast:
                    f.write(f"\n{value}")
                elif ast:
                    f.write(f"\n{tree}")
            if silent:
                # Print that it has been saved.
                click.echo(f"Saved in {filename}")
        # Else, simply print the result
        else:
            if not ast:
                click.echo(value)
            else:
                click.echo(tree)
        # If the option --nosave is not passed
        if not nosave:
            click.echo("Saving the input to operations.txt")
            # Then open operations.txt
            with open("operations.txt", "at") as f:
                # and save the just inputted operation
                if ast:
                    f.write(f"\n{operation} (ast)")
                else:
                    f.write(f"\n{operation}")
        # Else
        else:
            if verbose:
                # Print that it is not going to save to operations.txt
                click.echo("Will not save the operation in operations.txt")
    # Except is for catching errors
    except Exception as e:
        # Print error
        click.echo(e)


# Run the main function
if __name__ == "__main__":
    operate()
