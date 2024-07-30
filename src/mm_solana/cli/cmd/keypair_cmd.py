from pathlib import Path

import click
from mm_solana.account import (
    get_private_key_arr_str,
    get_private_key_base58,
    get_public_key,
)
from mm_std import print_console


@click.command(name="keypair", help="Print public, private_base58, private_arr by a private key")
@click.argument("private_key")
def cli(private_key: str) -> None:
    if (file := Path(private_key)).is_file():
        private_key = file.read_text()

    public = get_public_key(private_key)
    private_base58 = get_private_key_base58(private_key)
    private_arr = get_private_key_arr_str(private_key)
    print_console({"public": public, "private_base58": private_base58, "private_arr": private_arr}, print_json=True)