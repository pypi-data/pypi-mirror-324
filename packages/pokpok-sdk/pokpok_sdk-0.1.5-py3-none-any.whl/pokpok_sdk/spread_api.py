from web3.types import TxReceipt
from pokpok_sdk.utils import get_url
from pokpok_sdk.web3 import Web3
from pokpok_sdk.models import SpreadFetchResponse, SpreadQuoteFetchInput
from pokpok_sdk.web2 import Web2

class Spread:
    web2: Web2
    web3: Web3
    
    def __init__(self, api_key: str, rpc_url: str | None = None):
        api_url, rpc_url = get_url(api_key = api_key, rpc_url = rpc_url)
        
        self.web2 = Web2(api_key = api_key, base_url = api_url)
        self.web3 = Web3(rpc_url = rpc_url)
    
    def fetch_quote(self, input: SpreadQuoteFetchInput) -> SpreadFetchResponse:
        res = self.web2.fetch_quote(input, input.amount)
        return SpreadFetchResponse(**res)
        
        
    def place_order(self, fetch_quote_input: SpreadQuoteFetchInput, fetched_quote: SpreadFetchResponse) -> TxReceipt:
        quote = fetched_quote.data.quote
        amount = fetch_quote_input.amount
        quote_tuple, leg_tuples = self.web3.hatch_chicken_tuple(quote=quote, legs=fetched_quote.data.legs)
        
        tx_data_input = self.web3.tx_data_input(quote=quote)
        tx_data_builder = self.web3.contracts().hatchChickenWithSpread(
            quote_tuple,
            leg_tuples,
            amount
        )
        tx_data = tx_data_builder.build_transaction(tx_data_input)
            
        return self.web3.make_transaction(tx_data)

