"""
  @ Author:   Mr.Hat
  @ Date:     2024/3/21 02:44
  @ Description: 
  @ History:
"""
from data import config
from zeta_chain import ZetaChain
from zetachain_xp.utils import random_line, logger
import asyncio


async def retry_function(func, thread, address='', *args, **kwargs):
    while True:
        try:
            result = await func(*args, **kwargs)
            return result
        except Exception as e:
            for_address = f" 地址 {address}" if address else ''
            logger.error(f"函数执行错误 {func.__name__}{for_address}: {e}")
            await asyncio.sleep(10)


async def zeta_chain(thread):
    while True:
        act = await random_line('data/accounts.txt')
        if not act:
            break

        if '::' in act:
            private_key, proxy = act.split('::')
        else:
            private_key = act
            proxy = None

        zetachain = ZetaChain(key=private_key, thread=thread, proxy=proxy)

        # 邀请注册
        if not await zetachain.check_enroll():
            status, tx_hash = await retry_function(zetachain.enroll, thread, zetachain.web3_utils.acct.address)
            if status:
                logger.success(f"{zetachain.web3_utils.acct.address}:{tx_hash}")

                await asyncio.sleep(20)
                await zetachain.new_session()
            else:
                logger.error(f"{zetachain.web3_utils.acct.address}:{tx_hash}")

        # 向自己发送zeta
        if await zetachain.check_completed_task("SEND_ZETA") and config.SENDS_QUESTS['send_zeta'][1]:
            status, tx_hash, random_value = await retry_function(
                zetachain.transfer_zeta, thread, zetachain.web3_utils.acct.address)
            if status:
                logger.success(f"发送 {random_value} zeta {zetachain.web3_utils.acct.address}:{tx_hash}")
                await zetachain.sleep(config.DELAY['transaction'], logger, thread)
            else:
                logger.error(f"{zetachain.web3_utils.acct.address}:{tx_hash}")

        # 兑换BNB
        if await zetachain.check_completed_task("RECEIVE_BNB") and config.SENDS_QUESTS['send_bnb'][1]:
            status, tx_hash, random_value = await retry_function(
                zetachain.transfer_bnb, thread, zetachain.web3_utils.acct.address)
            if status:
                logger.success(f"{random_value} zeta -> bnb.bsc! {zetachain.web3_utils.acct.address}:{tx_hash}")
                await zetachain.sleep(config.DELAY['transaction'], logger, thread)
            else:
                logger.error(f"zeta -> bnb.bsc! {zetachain.web3_utils.acct.address}:{tx_hash}")

        # 兑换ETH
        if await zetachain.check_completed_task("RECEIVE_ETH") and config.SENDS_QUESTS['send_eth'][1]:
            status, tx_hash, random_value = await retry_function(
                zetachain.transfer_eth, thread, zetachain.web3_utils.acct.address)
            if status:
                logger.success(f"{random_value} zeta -> eth.eth! {zetachain.web3_utils.acct.address}:{tx_hash}")
                await zetachain.sleep(config.DELAY['transaction'], logger, thread)
            else:
                logger.error(f"zeta -> eth.eth! {zetachain.web3_utils.acct.address}:{tx_hash}")

        # 兑换BTC
        if await zetachain.check_completed_task("RECEIVE_BTC") and config.SENDS_QUESTS['send_btc'][1]:
            status, tx_hash, random_value = await retry_function(
                zetachain.transfer_btc, thread, zetachain.web3_utils.acct.address)
            if status:
                logger.success(f"{random_value} zeta -> btc.btc! {zetachain.web3_utils.acct.address}:{tx_hash}")
                await zetachain.sleep(config.DELAY['transaction'], logger, thread)
            else:
                logger.error(f"zeta -> btc.btc! {zetachain.web3_utils.acct.address}:{tx_hash}")

        # BNB授权
        if float(await zetachain.allowance_bnb()) + 0.001 < config.APPROVES['bnb_approve'][0]:
            status, tx_hash = await retry_function(
                zetachain.approve_bnb, thread, zetachain.web3_utils.acct.address)
            if status:
                logger.success(f"{zetachain.web3_utils.acct.address}:{tx_hash}")
                await zetachain.sleep(config.DELAY['transaction'], logger, thread)
            else:
                logger.error(f"{zetachain.web3_utils.acct.address}:{tx_hash}")

        # 添加BNB到流动性池
        if (await zetachain.check_completed_task("POOL_DEPOSIT_ANY_POOL") and
                zetachain.web3_utils.w3.from_wei(zetachain.web3_utils.balance_of_erc20(
                    zetachain.web3_utils.acct.address, '0x48f80608B672DC30DC7e3dbBd0343c5F02C738Eb'),
                    'ether') >= config.POOLS['send_bnb']):
            status, tx_hash = await retry_function(
                zetachain.add_liquidity, thread, zetachain.web3_utils.acct.address)
            if status:
                logger.success(f"zeta-bnb! {zetachain.web3_utils.acct.address}:{tx_hash}")
                await zetachain.sleep(config.DELAY['transaction'], logger, thread)
            else:
                logger.error(f"zeta-bnb! {zetachain.web3_utils.acct.address}:{tx_hash}")

        # eddy finance上兑换zeta为stzeta
        if await zetachain.check_completed_task("EDDY_FINANCE_SWAP"):
            status, tx_hash = await retry_function(
                zetachain.swap_zeta_to_stzeta, thread, zetachain.web3_utils.acct.address)
            if status:
                logger.success(f"zeta -> stzeta! {zetachain.web3_utils.acct.address}:{tx_hash}")
                await zetachain.sleep(config.DELAY['transaction'], logger, thread)
            else:
                logger.error(f"zeta -> stzeta! {zetachain.web3_utils.acct.address}:{tx_hash}")

        # 授权 stzeta
        if float(await zetachain.allowance_stzeta()) + 0.1 < config.APPROVES['stzeta_approve'][0]:
            status, tx_hash = await retry_function(
                zetachain.approve_stzeta, thread, zetachain.web3_utils.acct.address)
            if status:
                logger.success(f"{zetachain.web3_utils.acct.address}:{tx_hash}")
                await zetachain.sleep(config.DELAY['transaction'], logger, thread)
            else:
                logger.error(f"{zetachain.web3_utils.acct.address}:{tx_hash}")

        # 授权 wzeta
        if float(await zetachain.allowance_wzeta()) + 0.1 < config.APPROVES['wzeta_approve'][0]:
            status, tx_hash = await retry_function(
                zetachain.approve_wzeta, thread, zetachain.web3_utils.acct.address)
            if status:
                logger.success(f"{zetachain.web3_utils.acct.address}:{tx_hash}")
                await zetachain.sleep(config.DELAY['transaction'], logger, thread)
            else:
                logger.error(f"{zetachain.web3_utils.acct.address}:{tx_hash}")

        # 置换zeta为wzeta
        if await zetachain.get_wzeta_balance() < config.EDDY_SWAP['zeta_to_wzeta']:
            status, tx_hash = await retry_function(
                zetachain.swap_zeta_to_wzeta, thread, zetachain.web3_utils.acct.address)
            if status:
                logger.success(f"zeta -> wzeta! {zetachain.web3_utils.acct.address}:{tx_hash}")
                await zetachain.sleep(config.DELAY['transaction'], logger, thread)
            else:
                logger.error(f"zeta -> wzeta! {zetachain.web3_utils.acct.address}:{tx_hash}")

        if (await zetachain.check_completed_task("RANGE_PROTOCOL_VAULT_TRANSACTION") and
                await zetachain.get_stzeta_balance() >= config.POOLS['stzeta'] and await
                zetachain.get_wzeta_balance() >= config.EDDY_SWAP['zeta_to_wzeta'] and
                await zetachain.allowance_stzeta() >= config.POOLS['stzeta'] and
                await zetachain.allowance_wzeta() >= config.EDDY_SWAP['zeta_to_wzeta']):
            status, tx_hash = await retry_function(
                zetachain.add_liquidity_range, thread, zetachain.web3_utils.acct.address)
            if status:
                logger.success(
                    f"stzeta-wzeta! {zetachain.web3_utils.acct.address}:{tx_hash}")
                await zetachain.sleep(config.DELAY['transaction'], logger, thread)
            else:
                logger.error(f"stzeta-wzeta! {zetachain.web3_utils.acct.address}:{tx_hash}")

        if await zetachain.check_completed_task("ACCUMULATED_FINANCE_DEPOSIT"):
            # 将 zeta 交换为累积的 szeta
            if await zetachain.get_balance_stzeta_accumulated_finance() < config.ACCUMULATED_FINANCE['zeta_to_stzeta']:
                status, tx_hash = await retry_function(
                    zetachain.swap_zeta_to_stzeta_accumulated_finance, thread, zetachain.web3_utils.acct.address)
                if status:
                    logger.success(f"zeta -> stzeta! {zetachain.web3_utils.acct.address}:{tx_hash}")
                    await zetachain.sleep(config.DELAY['transaction'], logger, thread)
                else:
                    logger.error(f"zeta -> stzeta! {zetachain.web3_utils.acct.address}:{tx_hash}")

            # accumulated finance
            if float(await zetachain.allowance_stzeta_accumulated_finance()) + 0.1 < \
                    config.APPROVES['stzeta_accumulated_approve'][0]:
                status, tx_hash = await retry_function(
                    zetachain.approve_stzeta_accumulated_finance, thread, zetachain.web3_utils.acct.address)
                if status:
                    logger.success(f"{zetachain.web3_utils.acct.address}:{tx_hash}")
                    await zetachain.sleep(config.DELAY['transaction'], logger, thread)
                else:
                    logger.error(f"{zetachain.web3_utils.acct.address}:{tx_hash}")

            # wzeta 授权 zetaswap
            if await zetachain.allowance_stzeta_accumulated_finance() >= config.ACCUMULATED_FINANCE[
                'stzeta_to_wstzeta'] and await zetachain.get_balance_stzeta_accumulated_finance() >= \
                    config.ACCUMULATED_FINANCE['stzeta_to_wstzeta']:
                status, tx_hash = await retry_function(
                    zetachain.swap_stzeta_to_wstzeta_accumulated_finance, thread, zetachain.web3_utils.acct.address)
                if status:
                    logger.success(f"stzeta -> wstzeta! {zetachain.web3_utils.acct.address}:{tx_hash}")
                    await zetachain.sleep(config.DELAY['transaction'], logger, thread)
                else:
                    logger.error(f"stzeta -> wstzeta! {zetachain.web3_utils.acct.address}:{tx_hash}")

        # wzeta 授权 zetaswap
        if float(await zetachain.allowance_zetaswap_wzeta()) + 0.1 < config.APPROVES['zetaswap_wzeta_approve'][0]:
            status, tx_hash = await retry_function(
                zetachain.approve_zetaswap_wzeta, thread, zetachain.web3_utils.acct.address)
            if status:
                logger.success(
                    f"{zetachain.web3_utils.acct.address}:{tx_hash}")
                await zetachain.sleep(config.DELAY['transaction'], logger, thread)
            else:
                logger.error(f"{zetachain.web3_utils.acct.address}:{tx_hash}")

        # 通过 zetaswap 将 wzeta 交换到 eth.eth
        if await zetachain.check_completed_task("ZETA_SWAP_SWAP"):
            status, tx_hash = await retry_function(
                zetachain.zetaswap_wzeta_to_eth, thread, zetachain.web3_utils.acct.address)
            if status:
                logger.success(f"wzeta -> eth.eth! {zetachain.web3_utils.acct.address}:{tx_hash}")
                await zetachain.sleep(config.DELAY['transaction'], logger, thread)
            else:
                logger.error(f"wzeta -> eth.eth! {zetachain.web3_utils.acct.address}:{tx_hash}")

        # zeta链上的zeta stake
        if await zetachain.check_completed_task("ZETA_EARN_STAKE"):
            status, tx_hash = await retry_function(zetachain.stake_on_zetachain,
                                                   thread), zetachain.web3_utils.acct.address
            if status:
                logger.success(f"{zetachain.web3_utils.acct.address}:{tx_hash}")
                await zetachain.sleep(config.DELAY['transaction'], logger, thread)
            else:
                logger.error(f"{zetachain.web3_utils.acct.address}:{tx_hash}")

        # ultiverse上的徽章
        if await zetachain.check_completed_task("ULTIVERSE_MINT_BADGE"):
            status, tx_hash = await retry_function(
                zetachain.min_ultiverse_badge, thread, zetachain.web3_utils.acct.address)
            if status:
                logger.success(f"{zetachain.web3_utils.acct.address}:{tx_hash}")
                await zetachain.sleep(config.DELAY['transaction'], logger, thread)
            else:
                logger.error(f"{zetachain.web3_utils.acct.address}:{tx_hash}")

        # 领取已经完成的任务积分
        claimed = await zetachain.claim_tasks()
        if claimed:
            logger.success(f"{claimed} {zetachain.web3_utils.acct.address}")
        else:
            logger.warning(f"{zetachain.web3_utils.acct.address}")

        await zetachain.logout()
        await zetachain.sleep(config.DELAY['account'], logger, thread)

    logger.info(f"操作结束")


async def main():
    thread_count = min(10, int(input("输入线程数量 ")))
    # thread_count = 1

    tasks = []
    for thread in range(1, thread_count + 1):
        tasks.append(asyncio.create_task(zeta_chain(thread)))

    await asyncio.gather(*tasks)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
