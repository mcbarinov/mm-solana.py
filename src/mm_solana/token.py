from mm_std import Err, Ok, Result
from solana.rpc.api import Client
from solana.rpc.types import TokenAccountOpts
from solders.pubkey import Pubkey


def get_balance(node: str, owner_address: str, token_mint_address: str, token_account: str | None = None) -> Result[int]:
    try:
        client = Client(endpoint=node)
        if token_account:
            res_balance = client.get_token_account_balance(Pubkey.from_string(token_account))
            return Ok(int(res_balance.value.amount))

        res_accounts = client.get_token_accounts_by_owner(
            Pubkey.from_string(owner_address),
            TokenAccountOpts(mint=Pubkey.from_string(token_mint_address)),
        )
        if not res_accounts.value:
            return Err("no_token_accounts")

        token_accounts = [a.pubkey for a in res_accounts.value]
        balances = []
        for token_account_ in token_accounts:
            res = client.get_token_account_balance(token_account_)
            if res.value:  # type:ignore[truthy-bool]
                balances.append(int(res.value.amount))

        if len(balances) > 1:
            return Err("there are many non empty token accounts, set token_account explicitly")
        return Ok(balances[0])

    except Exception as e:
        return Err(e)


# def transfer_to_wallet_address(
#     *,
#     node: str,
#     private_key: str,
#     recipient_wallet_address: str,
#     token_mint_address: str,
#     amount: int,
# ) -> Result[str]:
#     try:
#         keypair = account.get_keypair(private_key)
#         token_client = Token(Client(node), Pubkey.from_string(token_mint_address), program_id=TOKEN_PROGRAM_ID, payer=keypair)
#
#         # get from_token_account
#         res = token_client.get_accounts(keypair.public_key)
#         token_accounts = res["result"]["value"]
#         if len(token_accounts) > 1:
#             return Result(error="many_from_token_accounts", data=res)
#         from_token_account = Pubkey.from_string(token_accounts[0]["pubkey"])
#
#         # get to_token_account
#         res = token_client.get_accounts(Pubkey.from_string(recipient_wallet_address))
#         token_accounts = res["result"]["value"]
#         if len(token_accounts) > 1:
#             return Result(error="many_to_token_accounts", data=res)
#         elif len(token_accounts) == 1:
#             to_token_account = Pubkey.from_string(token_accounts[0]["pubkey"])
#         else:  # create a new to_token_account
#             to_token_account = token_client.create_account(owner=Pubkey.from_string(recipient_wallet_address))
#
#         res = token_client.transfer(source=from_token_account, dest=to_token_account, owner=keypair, amount=amount)
#         if res.get("result"):
#             return Result(ok=res.get("result"), data=res)
#         return Result(error="unknown_response", data=res)
#     except RPCException as e:
#         return Result(error="rcp_exception", data=str(e))
#     except Exception as e:
#         return Result(error="exception", data=str(e))