import pytest
from unittest.mock import patch, Mock
from web3 import Web3
from pokpok_sdk import PokPokClient, PokPokError


@pytest.fixture
def web3_mock():
    with patch('web3.Web3') as mock:
        # Mock eth account
        mock.eth.account.from_key.return_value = Mock(address='0x742d35Cc6634C0532925a3b844Bc454e4438f44e')
        # Mock gas price
        mock.eth.gas_price = 20000000000
        # Mock nonce
        mock.eth.get_transaction_count.return_value = 1
        yield mock


@pytest.fixture
def client(web3_mock):
    return PokPokClient(
        api_url="https://api.pokpok.io",
        api_key="test-key",
        web3_provider="https://mainnet.infura.io/v3/your-project-id",
        contract_address="0x742d35Cc6634C0532925a3b844Bc454e4438f44e",
        private_key="0x0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef"
    )


def test_client_initialization(client):
    assert client.api_url == "https://api.pokpok.io"
    assert client.api_key == "test-key"
    assert "Authorization" in client.session.headers
    assert client.session.headers["Authorization"] == "Bearer test-key"


@patch('requests.Session.request')
def test_get_quote_success(mock_request, client):
    expected_response = {
        "quote_id": "q123",
        "premium": 0.05,
        "strike": 50000
    }
    
    mock_response = Mock()
    mock_response.json.return_value = expected_response
    mock_request.return_value = mock_response
    
    response = client.get_quote("BTC", 1.0, "3d")
    
    assert response == expected_response
    mock_request.assert_called_once_with(
        "POST",
        "https://api.pokpok.io/quote",
        json={"underlying": "BTC", "size": 1.0, "tenor": "3d"}
    )


def test_place_order_success(client, web3_mock):
    # Mock contract function calls
    contract_mock = Mock()
    contract_mock.functions.placeOrder().estimate_gas.return_value = 100000
    web3_mock.eth.contract.return_value = contract_mock
    
    # Mock transaction receipt
    tx_receipt = {
        'transactionHash': bytes.fromhex('1234' * 16),
        'status': 1,
        'blockNumber': 12345,
        'gasUsed': 100000
    }
    web3_mock.eth.wait_for_transaction_receipt.return_value = tx_receipt
    
    response = client.place_order("q123")
    
    assert response['status'] == 'confirmed'
    assert response['transaction_hash'] == '1234' * 16
    assert response['block_number'] == 12345
    assert response['gas_used'] == 100000


def test_place_order_without_private_key():
    client = PokPokClient(
        api_url="https://api.pokpok.io",
        api_key="test-key",
        web3_provider="https://mainnet.infura.io/v3/your-project-id",
        contract_address="0x742d35Cc6634C0532925a3b844Bc454e4438f44e"
    )
    
    with pytest.raises(PokPokError, match="Private key is required to place orders"):
        client.place_order("q123")


@patch('requests.Session.request')
def test_api_error_handling(mock_request, client):
    mock_request.side_effect = Exception("API Error")
    
    with pytest.raises(PokPokError):
        client.get_quote("BTC", 1.0, "3d") 