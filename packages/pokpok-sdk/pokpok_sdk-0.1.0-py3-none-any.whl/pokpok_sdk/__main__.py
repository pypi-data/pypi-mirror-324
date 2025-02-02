from pokpok_sdk.exceptions import PokPokError
from . import PaygApi, SpreadApi, SpreadQuoteFetchInput, QuoteFetchInput, Web2, Web3

spread_input = SpreadQuoteFetchInput(
    duration=3,
    meal="economical",
    coin="eth",
    option="up",
    size=0.5,
    spreadPercent=5,
    amount=1
)

payg_input = QuoteFetchInput(
    duration=3,
    meal="economical",
    coin="eth",
    option="up",
    size=0.5,
    amount=1
)

web2 = Web2(api_key='live_yYgaVBNhQzvqLX3F9sexN_wUxgDZQNlWmlceFlXXwRv')
web3 = Web3(alchemy_key='7tdqjb0B5f9acZgFjs0OC4h4At7oiUEd')
def run_payg_example():
    api = PaygApi(web2=web2, web3=web3)
    
    fetched_quote = api.fetch_quote(
        input=payg_input
    )
    tx_receipt = api.place_order(
        fetch_quote_input=payg_input, 
        fetched_quote=fetched_quote
    )
    print(f"Transaction Receipt: {tx_receipt}")


def run_spread_example():
    api = SpreadApi(web2=web2, web3=web3)

    fetched_quote = api.fetch_quote(
        input=spread_input
    )
    tx_receipt = api.place_order(
        fetch_quote_input=spread_input,
        fetched_quote=fetched_quote
    )
    print(f"Transaction Receipt: {tx_receipt}")

try:  
    # run_payg_example()
    run_spread_example()
except PokPokError as e:
    print(f"Error: {e}")