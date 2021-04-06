from web3 import Web3

w3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/c950d3e5f5c34411a5523c0b6b612d44'))
account = w3.eth.account.create()
privateKey = account.privateKey.hex()
address = account.address