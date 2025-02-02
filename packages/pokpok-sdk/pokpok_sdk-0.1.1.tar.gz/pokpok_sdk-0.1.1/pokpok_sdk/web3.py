from decimal import Decimal
import json
from typing import Any
from web3 import Web3 as W3
from web3.types import Wei, TxReceipt

from pokpok_sdk.config import MERCHANT_PKEY, PROTOCOL_PROXY_ADDRESS
from pokpok_sdk.constants import ALCHEMY_URL, PROTOCOL_JSON
import os

from pokpok_sdk.models import Quote

class Web3:
    w3: W3
    account: Any
    contract: Any
    
    def __init__(self, alchemy_key:str, merchant_key: str = MERCHANT_PKEY, protocal_proxy_address: str = PROTOCOL_PROXY_ADDRESS, alchemy_url: str = ALCHEMY_URL, protocol_json: str = PROTOCOL_JSON):
        self.w3 = W3(W3.HTTPProvider(f"{alchemy_url}/{alchemy_key}"))
        self.account = self.w3.eth.account.from_key(merchant_key)
     
        script_dir = os.path.dirname(os.path.abspath(__file__))
        abi_path = os.path.join(script_dir, protocol_json)
        
        with open(abi_path) as f:   
            abi = json.load(f)
    
        self.contract = self.w3.eth.contract(
            address=self.w3.to_checksum_address(protocal_proxy_address),
            abi=abi
        )

    def to_wei(self, eth_amount: float) -> Wei:
        return self.w3.to_wei(Decimal(eth_amount), 'ether')

    def to_ether(self, wei_amount: int) -> Decimal:
        return W3.from_wei(int(wei_amount), 'ether')

    def contracts(self):
        return self.contract.functions
    
    def tx_data_input(self, quote: Quote) -> dict:
        upfrontPaymentEth = self.to_ether(quote.upfrontPayment)
        sizeEth = self.to_ether(quote.size)
        totalEth = upfrontPaymentEth * sizeEth
        totalWei = self.to_wei(totalEth)
        gas_price = self.w3.eth.gas_price
        
        return {
            'from': self.account.address,
            'value': totalWei,
            'nonce': self.w3.eth.get_transaction_count(self.account.address),
            'maxFeePerGas': gas_price * 2,  
            'maxPriorityFeePerGas': gas_price,
            'chainId': 84532,  
        }
        
    def make_transaction(self, tx_data: Any) -> TxReceipt:
        estimated_gas = self.w3.eth.estimate_gas(tx_data)
        tx_data['gas'] = int(estimated_gas * 1.2)

        signed_tx = self.account.sign_transaction(tx_data)
        tx_hash = self.w3.eth.send_raw_transaction(signed_tx.raw_transaction)
        
        return self.w3.eth.wait_for_transaction_receipt(tx_hash, timeout=120)
        

    def hatch_chicken_tuple(self, quote: Quote, legs: list[Quote] = []) -> Any:
        feeding_schedule = [
            (int(fs.amount), int(fs.dueOn), fs.fed)
            for fs in quote.feedingSchedule
        ]

        quote_tuple = (
            quote.creator,
            int(quote.asset),
            int(quote.spotPrice),
            int(quote.strikePrice),
            int(quote.size),
            int(quote.upfrontPayment),
            [int(cs) for cs in quote.commissionSchedule],
            int(quote.side),
            int(quote.maturityTimestamp),
            int(quote.feedCurrency),
            quote.signature,
            feeding_schedule,
            quote.issuer,
            quote.settled,
            int(quote.quoteTime)
        )

        if legs:
            legs_tuple = [
                (
                    int(leg.strike),
                    int(leg.size),
                    int(leg.side),
                    int(leg.position),
                )
                for leg in legs
            ]
        else:
            legs_tuple = None
        
        return quote_tuple, legs_tuple
        
        