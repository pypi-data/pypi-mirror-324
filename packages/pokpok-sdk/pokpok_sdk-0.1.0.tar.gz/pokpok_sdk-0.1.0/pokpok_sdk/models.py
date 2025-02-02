from typing import List, Literal
from pydantic import BaseModel, model_validator

class FeedingSchedule(BaseModel):
    amount: str
    dueOn: int
    fed: bool

class Leg(BaseModel):
    side: int
    position: int
    strike: str
    size: str

class Quote(BaseModel):
    creator: str
    asset: int
    spotPrice: str
    strikePrice: str
    size: str
    upfrontPayment: str
    commissionSchedule: List[str]
    side: int
    maturityTimestamp: str
    feedCurrency: int
    signature: str
    feedingSchedule: List[FeedingSchedule]
    issuer: str
    settled: bool
    quoteTime: int
    
class QuoteFetchInput(BaseModel):
    duration: Literal[3, 7]
    meal: Literal["economical", "nourished"]
    coin: Literal["eth", "btc"]
    option: Literal["up", "down"]
    size: Literal[0.5, 1]
    type: Literal["payg", "spread"] = "payg"
    amount: int

class SpreadQuoteFetchInput(BaseModel):
    duration: Literal[3, 7]
    meal: Literal["economical", "nourished"]
    coin: Literal["eth", "btc"]
    option: Literal["up", "down"]
    size: Literal[0.5, 1]
    type: Literal["spread", "payg"] = "spread"
    amount: int
    spreadPercent: Literal[5, 10]

    @model_validator(mode="after")
    def check_spread_percent(cls, values):
        if values.type == "spread" and values.spreadPercent is None:
            raise ValueError("spreadPercent is required when type is 'spread'")
        return values
    
class QuoteData(BaseModel):
    quote: Quote
    
class QuoteFetchResponse(BaseModel):
    status: str
    message: str
    data: QuoteData
    
    
class SpreadData(BaseModel):
    quote: Quote
    legs: List[Leg]
    

class SpreadFetchResponse(BaseModel):
    status: str
    message: str
    data: SpreadData
    
