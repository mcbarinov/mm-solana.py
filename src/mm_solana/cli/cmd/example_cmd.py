from pathlib import Path

import click


@click.command(name="example", help="Print config or arg example for a module and exit")
@click.argument("module", type=click.Choice(["balance", "transfer-sol"]))
def cli(module: str) -> None:
    example_file = Path(Path(__file__).parent.absolute(), "../examples", f"{module}.yml")
    click.echo(example_file.read_text())
