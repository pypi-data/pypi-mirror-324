# PokPok SDK

A Python SDK for interacting with PokPok's options trading platform. This SDK provides easy access to both Pay-as-you-go (PAYG) and Spread trading functionalities.

## Installation

Install the package using pip:

```bash
pip install pokpok-sdk
```

## Configuration

The SDK requires some environment variables to be set up. Create a `.env` file in your project root:

```env
MERCHANT_PKEY=your_private_key_here
```

## Usage

### Initialize Clients

You can initialize both PAYG and Spread clients with your API key. Optionally, you can provide a custom RPC URL:

```python
from pokpok_sdk import Payg, Spread

# Basic initialization
payg = Payg(api_key='your_api_key')
spread = Spread(api_key='your_api_key')

# With custom RPC URL
payg = Payg(api_key='your_api_key', rpc_url='your_custom_rpc_url')
spread = Spread(api_key='your_api_key', rpc_url='your_custom_rpc_url')
```

### PAYG Trading Example

```python
from pokpok_sdk import Payg, QuoteFetchInput
from pokpok_sdk.exceptions import PokPokError

# Create input for quote fetching
payg_input = QuoteFetchInput(
    duration=3,
    meal="economical",
    coin="eth",
    option="up",
    size=0.5,
    amount=1
)

# Execute PAYG trade
try:
    payg = Payg(api_key='your_api_key')

    # Fetch quote
    fetched_quote = payg.fetch_quote(input=payg_input)

    # Place order
    tx_receipt = payg.place_order(
        fetch_quote_input=payg_input,
        fetched_quote=fetched_quote
    )
    print(f"Transaction Receipt: {tx_receipt}")
except PokPokError as e:
    print(f"Error: {e}")
```

### Spread Trading Example

```python
from pokpok_sdk import Spread, SpreadQuoteFetchInput
from pokpok_sdk.exceptions import PokPokError

# Create input for spread quote fetching
spread_input = SpreadQuoteFetchInput(
    duration=3,
    meal="economical",
    coin="eth",
    option="up",
    size=0.5,
    spreadPercent=5,
    amount=1
)

# Execute Spread trade
try:
    spread = Spread(api_key='your_api_key')

    # Fetch quote
    fetched_quote = spread.fetch_quote(input=spread_input)

    # Place order
    tx_receipt = spread.place_order(
        fetch_quote_input=spread_input,
        fetched_quote=fetched_quote
    )
    print(f"Transaction Receipt: {tx_receipt}")
except PokPokError as e:
    print(f"Error: {e}")
```

## Input Parameters

### QuoteFetchInput

- `duration`: Trading duration `3 or 7` days
- `meal`: Trading strategy type (e.g., "economical")
- `coin`: Trading pair (e.g., "eth")
- `option`: Option type ("up" or "down")
- `size`: Position size
- `amount`: Trading amount

### SpreadQuoteFetchInput

Includes all parameters from QuoteFetchInput plus:

- `spreadPercent`: Spread percentage for the trade

## Error Handling

The SDK uses custom `PokPokError` for error handling. Always wrap your API calls in try-except blocks:

```python
from pokpok_sdk.exceptions import PokPokError

try:
    # Your SDK calls here
except PokPokError as e:
    print(f"Error: {e}")
```

## License

MIT

## Support

For support, please contact support@pokpok.io
