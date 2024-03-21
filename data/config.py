"""
  @ Author:   Mr.Hat
  @ Date:     2024/3/21 02:25
  @ Description: 
  @ History:
"""
# 邀请地址
REF_LINK = 'https://hub.zetachain.com/zh-CN/xp?code=YWRkcmVzcz0weDVBNTA1QTE4MjhFOTEyRTkwYUQ4NDlhNzVEOEI1Y0IzMjdCRDgyNWEmZXhwaXJhdGlvbj0xNzEzNTUyMTMyJnI9MHgyNmU2ZTJmYjA5NThlMzcwMjFmZjIyZTA0NTM4MDg3NWYyMWU3YTY1OGYzOWMwMTI5MmQxOTZmMjNiMzZjMDE1JnM9MHgxMDNiYjgxMjkxYWQ2ZjhhMjlmZDk2ZTE5ZDdiZTE2YWZkODNlZmE2N2U0NjAzODU1NDdiOWFjNmM0MWMzYmUzJnY9Mjg%3D'

# api key native.org.
NATIVE_API_KEY = "c808b0f365815149b7982b1bc6e19ed9d9fb00c5"

# 延时配置
DELAY = {
    "account": (5, 10),       # 账户与账户之间的延时配置
    "transaction": (20, 30),  # 事物之间的延时操作
}

# 授权配置. [x,y]. х - 最小值, у - 最大值.
APPROVES = {
    "bnb_approve": [11, 20],  # 授权的BNB数量
    "stzeta_approve": [12, 20],  # 授权的stzeta数量
    "wzeta_approve": [12, 20],   # 授权的wzeta数量
    "stzeta_accumulated_approve": [12, 20],
    "zetaswap_wzeta_approve": [12, 20]
}

# 转账范围配置
SENDS_QUESTS = {
    "send_zeta": [0.001, 0.01],         # 发送的zeta数量范围
    "send_bnb":  [0.01, 0.002],     # zeta兑换bnb的数量范围 zeta->bnb.bsc (izumi)
    "send_eth":  [0.0001, 0.0002],    # zeta兑换eth的数量范围 zeta->eth.rth (izumi)
    "send_btc":  [0.001, 0.002],     # zeta兑换btc的数量范围 zeta->btc.btc (izumi)
}

# 流动池配置
POOLS = {
    "send_bnb": 0.00001,       # 添加到流动性池的BNB数量
    "send_zeta": 0.0001,      # 添加到流动性池的zeta数量

    # range pool
    "stzeta": 0.001
}

# app.eddy.finance/swap
EDDY_SWAP = {
    "zeta_to_stzeta": 0.0013,  # stzeta上Swap的Zeta数量
    "zeta_to_wzeta": 0.01,   # wzeta 上交换的 zeta 数量，最多不超过 zeta_to_stzeta
}

# Accumulated finance
ACCUMULATED_FINANCE = {
    "zeta_to_stzeta": 0.0001,     # 用于交换到 szeta 到累积资金的 zeta 数量
    "stzeta_to_wstzeta": 0.0001  # 用于交换到 wstzeta 以积累资金的 szeta 数量不应超过 zeta_to_stzeta
}

# ZetaChain
STAKE_ZETACHAIN= {
    "zeta_count": 0.0011
}

# 通过 zetaswap 将 wzeta 交换为 ETH.ETH。
# [x，y] x - 最小数量，y - 最大数量。随机最多 5 位数字
ZETASWAP = {
    "wzeta_count": [0.0001, 0.0002]
}

RPCs = {
    "zetachain": "https://zetachain-evm.blockpi.network/v1/rpc/public"  # zetachain rpc
}