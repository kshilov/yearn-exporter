from yearn.v2.registry import Registry
from brownie.exceptions import BrownieEnvironmentWarning
from click import secho, style
from toolz import compose
from toolz.curried import get, pluck, groupby, valmap
from pprint import pprint

def main():
    raise Exception("Not implemented yet, call print_earnings")

def print_earnings():
    registry = Registry()
    registry.load_strategies()

    earnings = []
    for vault in registry.vaults:
        for strategy in vault.strategies:
            contract = strategy.strategy
            strategist = getattr(contract, "strategist", None)

            if strategist:
                config = vault.vault.strategies(contract).dict()
                if config.get("performanceFee"):
                    earnings.append({
                        "strategist": strategist(),
                        **config
                    })

    if earnings:
        print("....All earnings:")
        pprint(earnings)
        data = valmap(compose(lambda fg: sum(gain / fee for fee, gain in fg),
                              pluck(["performanceFee", "totalGain"])),
                      groupby("strategist", earnings))
        print("....Earnings grouped by strategist")
        pprint(data)
    else:
        print("No earnings found")
