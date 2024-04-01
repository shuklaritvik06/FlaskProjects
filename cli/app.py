from flask import Flask
import click

app = Flask(__name__)


@app.cli.command()
def hello():
    """Prints a hello message."""
    print("Hello, World!")


@app.cli.command()
def goodbye():
    """Prints a goodbye message."""
    print("Goodbye, World!")


@app.cli.command()
@click.argument("name")
def greet(name):
    """Greets a person by name."""
    print(f"Hello, {name}!")


@app.cli.command()
@click.option("--verbose", is_flag=True, help="Print verbose output.")
def debug(verbose):
    """Runs in debug mode."""
    if verbose:
        print("Running in debug mode.")
    else:
        print("Running in normal mode.")


@app.cli.command()
@click.option("--name", default="World", help="Specify a name.")
def echo(name):
    """Echos a name."""
    print(f"You said: {name}")


if __name__ == "__main__":
    app.run(debug=True)
