from pokpok_sdk.constants import BASE_RPC_URL, BASE_SEPOLIA_RPC_URL, LIVE_URL, STAGING_URL

def get_url(api_key: str, rpc_url: str | None = None) -> tuple[str, str]:    
    if api_key.startswith("live_"):
        return (LIVE_URL, rpc_url or BASE_RPC_URL)
    elif api_key.startswith("sandbox_"):
        return (STAGING_URL, rpc_url or BASE_SEPOLIA_RPC_URL)
    else:
        raise ValueError(f"Invalid API Key: {api_key}")
