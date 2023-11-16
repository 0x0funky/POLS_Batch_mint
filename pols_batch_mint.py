from web3 import Web3,Account

rpc='https://rpc-mainnet.maticvigil.com/'
to_address = '' #這邊填你的地址
private_key='' #你錢包的私鑰
lim=1000 #你要打的次數 (中間可能會有失敗的，如果全部打完沒有1000就再重跑一次)


w3 = Web3(Web3.HTTPProvider(rpc))
from_address = Account.from_key(private_key).address
print('WEB3 Connected',w3.isConnected())

if w3.isConnected() ==True:
    nonce=w3.eth.get_transaction_count(from_address)
    
    for i in range(lim):
        gas_price = w3.eth.gas_price
        gas_price_gwei = w3.fromWei(gas_price, 'Gwei')
        data = 'data:,{"p":"prc-20","op":"mint","tick":"pols","amt":"100000000"}'
        print("Nonce:",nonce,"GAS:",gas_price_gwei,'Address to:',from_address)
        transaction = {
            'from': from_address,  
            'to': to_address,  
            'value': w3.toWei(0, 'ether'),  
            'nonce': nonce,  
            'gas': 25000,  
            'gasPrice': int(gas_price*1.025),  
            'data': w3.toHex(text=data),  
            'chainId': w3.eth.chain_id  
        }

        signed = w3.eth.account.sign_transaction(transaction, private_key)
        try:
            tx_hash = w3.eth.send_raw_transaction(signed.rawTransaction)
            print("Hash:", tx_hash.hex(),'noce:',nonce)
        except Exception as e:
            print('Error on tx',e,'Error data：',data)
        nonce+=1