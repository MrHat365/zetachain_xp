"""
  @ Author:   Mr.Hat
  @ Date:     2024/3/21 15:50
  @ Description: OKX注册地址：https://www.ouxyi.style/join/TOTHEMOON25
                 ZETA OKX转账功能
  @ History:
"""
import os

import ccxt
import time
import random
from loguru import logger
from web3 import Web3

API_KEY = ''  # Enter api_key
SECRET = ''  # Enter secret
PASSPHRASE = ''  # Enter passphrase

TOKEN = 'ZETA'  # token种类
NETWORK = 'ZetaChain'  # 公链名称
# AMOUNT = round(random.uniform(1.0, 1.5), 6)  # 随机数量的ZETA，也可以自定义
AMOUNT = 2  # 随机数量的ZETA，也可以自定义


MIN_DELAY = 20  # Min seconds for delay between withdraws
MAX_DELAY = 50  # Max seconds for delay between withdraws


RESERVED_AMOUNT = 0.1  # 钱包需要保留的token数量
EXCHANGE_ADDRESS = ""  # 需要转到交易所的充币地址


exchange = ccxt.okx({
    'apiKey': API_KEY,
    'secret': SECRET,
    'password': PASSPHRASE,
    'enableRateLimit': True,
})


def token_fee(token, network):
    info = exchange.fetch_currencies()
    network_fee = info[token]['networks'][network]['fee']
    return network_fee


def withdraw_info(value, wallet, token, amount, network):
    if value == 'success':
        result = f"**** Succesfull withdrawal {amount} {token} to {wallet} on {network} network ****"
        return result
    elif value == 'error':
        result = f"**** Withdrawal error ****"
        return result


def withdraw(token, network, amount, wallet):
    network_fee = token_fee(token, network)

    try:
        exchange.withdraw(token, amount, wallet, params={
            'toAddress': wallet,
            'chainName': network,
            'dest': 4,
            'fee': network_fee,
            'pwd': '-',
            'amt': amount,
            'network': network
        })

        logger.success(withdraw_info('success', wallet, token, amount, network))
    except Exception as e:
        logger.error(withdraw_info('error', wallet, token, amount, network))


def main():
    current_directory = os.path.dirname(os.path.abspath(__file__))
    # 从多个文件中读取钱包数据
    file_name = os.path.join(current_directory, "data", "wallets.txt")
    with open(file_name, 'r') as f:
        wallets_list = [row.strip() for row in f]
    for wallet in wallets_list:
        withdraw(TOKEN, NETWORK, AMOUNT, wallet)
        delay = random.uniform(MIN_DELAY, MAX_DELAY)
        time.sleep(delay)


def create_web3_with_proxy(rpc_endpoint, proxy=None):
    if proxy is None:
        return Web3(Web3.HTTPProvider(rpc_endpoint))

    proxy_type = proxy.split(":")[0]
    request_kwargs = {"proxies": {proxy_type: proxy}}

    return Web3(Web3.HTTPProvider(rpc_endpoint, request_kwargs=request_kwargs))


def current_time():
    cur_time = time.strftime("%Y-%m-%d %H:%M:%S")[:-3]
    return cur_time


def transaction(private_key: str, to_: str, proxy=None) -> str:
    """ 将钱包多余资产转回交易所
    :param private_key:
    :param to_:
    :param proxy:
    :return:
    """
    transactions_break_time = 2

    web3 = create_web3_with_proxy("https://zetachain-mainnet-archive.allthatnode.com:8545", proxy)
    account = web3.eth.account.from_key(private_key)

    balance = float(int(web3.eth.get_balance(account.address)) / 1000000000000000000)
    logger.success(f"账户: {account.address}, 当前资产: {balance}, 可划转资产： {float(balance - RESERVED_AMOUNT)}")

    if balance > RESERVED_AMOUNT:
        tx = {
            "from": account.address,
            "to": web3.to_checksum_address(to_),
            "value": web3.to_wei(float(balance - RESERVED_AMOUNT), "ether"),
            "nonce": web3.eth.get_transaction_count(account.address),
            "gasPrice": web3.eth.gas_price,
            "chainId": 7000,
        }
        tx["gas"] = int(web3.eth.estimate_gas(tx))
        signed_txn = web3.eth.account.sign_transaction(tx, private_key)
        transaction_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction).hex()
        print(f"{current_time()} | Waiting for Self transfer TX to complete...")
        receipt = web3.eth.wait_for_transaction_receipt(transaction_hash)
        if receipt.status != 1:
            print(f"{current_time()} | Transaction {transaction_hash} failed!")
            time.sleep(transactions_break_time)
        print(f"{current_time()} | Send & Receive TX hash: {transaction_hash}")
        time.sleep(transactions_break_time)


def back_to_exchange(address: str):
    """ 将钱包多余资产转回交易所地址
    :param address: 交易所冲币地址
    :return:
    """
    current_directory = os.path.dirname(os.path.abspath(__file__))
    # 从多个文件中读取钱包数据
    file_name = os.path.join(current_directory, "data", "temp_wallets.txt")

    with open(file_name, 'r') as f:
        privates_list = [row.strip() for row in f]
    for private in privates_list:
        transaction(private, address)


if __name__ == '__main__':

    back_to_exchange(EXCHANGE_ADDRESS)

    # main()
