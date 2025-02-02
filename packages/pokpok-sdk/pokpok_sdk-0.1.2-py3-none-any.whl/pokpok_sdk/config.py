from dotenv import load_dotenv
import os 

load_dotenv()

ALCHEMY_KEY = os.getenv('ALCHEMY_KEY')
MERCHANT_PKEY = os.getenv('MERCHANT_PKEY')
PROTOCOL_PROXY_ADDRESS = os.getenv('PROTOCOL_PROXY_ADDRESS')
