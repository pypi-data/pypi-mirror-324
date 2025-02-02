# PokPok SDK
pokpok_sdk/
├── pyproject.toml
├── README.md
├── src/
│   └── pokpok_sdk/
│       ├── __init__.py
│       ├── client.py
│       ├── models.py
│       ├── exceptions.py
│       └── constants.py
└── tests/
    ├── __init__.py
    └── test_client.py

# pyproject.toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "pokpok_sdk"
version = "0.1.0"
authors = [
    { name = "Your Name", email = "your.email@example.com" },
]
description = "PokPok SDK for accessing quote services"
readme = "README.md"
requires-python = ">=3.8"
dependencies = [
    "pydantic>=2.0.0",
    "requests>=2.28.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0.0",
    "black>=22.0.0",
    "isort>=5.0.0",
]

# README.md
# PokPok SDK

A Python SDK for interacting with PokPok's quote services.

## Installation

```bash
pip install pokpok_sdk
```

## Usage

```python
from pokpok_sdk import PokPokClient, QuoteRequest

client = PokPokClient(api_key="your-api-key")
request = QuoteRequest(
    duration=3,
    meal="economical",
    coin="btc",
    option="up",
    size=1,
    type="payg"
)

quote = client.get_quote(request)
print(quote.data.spot_price)
```

## Development

1. Clone the repository
2. Install development dependencies: `pip install -e ".[dev]"`
3. Run tests: `pytest`