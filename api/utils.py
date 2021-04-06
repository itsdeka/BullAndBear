from web3 import Web3

def sendTransaction(message):
    w3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/c950d3e5f5c34411a5523c0b6b612d44'))
    address = '0xdFcF33Ee2439CbB6a8a86811b6E7DED462b98af2'
    privateKey = '0x5e18c69fd8e6c74aa5fb481a9aa75a7c31a54752221de69528b417abd2d4dfa6'
    nonce = w3.eth.getTransactionCount(address)
    gasPrice = w3.eth.gasPrice
    value = w3.toWei(0, 'ether')
    signedTx = w3.eth.account.signTransaction(dict(
        nonce=nonce,
        gasPrice=gasPrice,
        gas= 100000,
        to='0x0000000000000000000000000000000000000000',
        value=value,
        data=message.encode('utf-8')
    ), privateKey)

    tx = w3.eth.sendRawTransaction(signedTx.rawTransaction)
    txId = w3.toHex(tx)
    return txId