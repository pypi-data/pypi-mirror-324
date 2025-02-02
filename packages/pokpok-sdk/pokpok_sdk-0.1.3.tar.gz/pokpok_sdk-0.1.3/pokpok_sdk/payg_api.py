import requests
from web3 import Web3
from web3.types import Wei, TxReceipt
from pokpok_sdk.web3 import Web3
from pokpok_sdk.models import QuoteFetchInput, QuoteFetchResponse
from pokpok_sdk.web2 import Web2

class PaygApi:
    web2: Web2
    web3: Web3
    
    def __init__(self, web2: Web2, web3: Web3):
        self.web2 = web2
        self.web3 = web3
    
    def fetch_quote(self, input: QuoteFetchInput) -> QuoteFetchResponse:
        res = self.web2.fetch_quote(input, input.amount)
        return QuoteFetchResponse(**res)
        
        
    def place_order(self, fetch_quote_input: QuoteFetchInput, fetched_quote: QuoteFetchResponse) -> TxReceipt:
        quote = fetched_quote.data.quote
        amount = fetch_quote_input.amount
        quote_tuple, _ = self.web3.hatch_chicken_tuple(quote=quote)
        
        tx_data_input = self.web3.tx_data_input(quote=quote)
        tx_data_builder = self.web3.contracts().hatchChicken(quote_tuple, amount)
        tx_data = tx_data_builder.build_transaction(tx_data_input)
            
        return self.web3.make_transaction(tx_data)

