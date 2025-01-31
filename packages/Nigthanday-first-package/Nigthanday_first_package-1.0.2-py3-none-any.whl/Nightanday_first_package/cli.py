import click
import os

@click.group()
def cli():
    """🔥 This is my main CLI group ! 🔥"""
    pass

@click.argument("directory", default='.')
@cli.command()
def show(directory):
    """Recursively prints all files and subfolders in the given directory."""

    def helper(directory, indent=0):
        try:
            for item in os.listdir(directory):
                item = str(item)
                path = os.path.join(directory, item)
                if os.path.isdir(path):
                    click.echo("  " * indent + "|- 📁 " + item)  # Indentation for structure
                    helper(path, indent + 1)
                else:
                    click.echo("  " * indent + "|- " + item)
        except PermissionError:
            click.echo("  " * indent + "|- [Access Denied]")

    # Run the function in the current directory
    helper(directory)

# Run click cli
if __name__ == "__main__":
    cli()