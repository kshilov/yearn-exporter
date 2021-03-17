from brownie import Contract, ZERO_ADDRESS
from yearn.cache import memory
from cachetools.func import ttl_cache
from yearn.prices import magic

curve_registry = Contract("0x7D86446dDb609eD0F5f8684AcF30380a356b2B4c")

# fold underlying tokens into one of the basic tokens
BASIC_TOKENS = {
    "0x6B175474E89094C44Da98b954EedeAC495271d0F",  # dai
    "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",  # weth
    "0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE",  # eth
    "0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599",  # wbtc
    "0xD71eCFF9342A5Ced620049e616c5035F1dB98620",  # seur
    "0x514910771AF9Ca656af840dff83E8264EcF986CA",  # link
}


@memory.cache()
def is_curve_lp_token(token):
    pool = curve_registry.get_pool_from_lp_token(token)
    return pool != ZERO_ADDRESS


@memory.cache()
def underlying_coins(token):
    pool = curve_registry.get_pool_from_lp_token(token)
    coins = curve_registry.get_underlying_coins(pool)
    return [coin for coin in coins if coin != ZERO_ADDRESS]


@ttl_cache(ttl=600)
def price(token, block=None):
    coins = underlying_coins(token)
    print(token, coins)
    try:
        coin = (set(coins) & BASIC_TOKENS).pop()
    except KeyError:
        coin = coins[0]

    virtual_price = curve_registry.get_virtual_price_from_lp_token(token, block_identifier=block) / 1e18
    return magic.price(coin, block=block) * virtual_price