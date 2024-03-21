"""
  @ Author:   Mr.Hat
  @ Date:     2024/3/21 15:50
  @ Description: OKX注册地址：https://www.ouxyi.style/join/TOTHEMOON25
                 ZETA OKX转账功能
  @ History:
"""
import ccxt
import time
import random
from utils.logger import logger

API_KEY = 'api_key'  # Enter api_key
SECRET = 'secret'  # Enter secret
PASSPHRASE = 'passphrase'  # Enter passphrase

TOKEN = 'ZETA'  # token种类
NETWORK = 'ZETA-ZetaChain'  # 公链名称
AMOUNT = round(random.uniform(1.0, 1.5), 6)  # 随机数量的ZETA，也可以自定义

MIN_DELAY = 20  # Min seconds for delay between withdraws
MAX_DELAY = 50  # Max seconds for delay between withdraws

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
    with open('wallets.txt', 'r') as f:
        wallets_list = [row.strip() for row in f]
    for wallet in wallets_list:
        withdraw(TOKEN, NETWORK, AMOUNT, wallet)
        delay = random.uniform(MIN_DELAY, MAX_DELAY)
        time.sleep(delay)


if __name__ == '__main__':
    main()
