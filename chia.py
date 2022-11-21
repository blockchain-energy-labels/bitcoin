import requests

price_api_url = "https://xchscan.com/api/chia-price"
block_trans_api_url = "https://xchscan.com/api/block/txns?hash=0xe64b82f2af6b7ab341fcb66dfeb42d54cdcc689928130d0ad3d58763ece49b1b&limit=10&offset=0"
response = requests.get(block_trans_api_url)
print(response.json())