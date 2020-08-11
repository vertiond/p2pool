import os
import platform

from twisted.internet import defer

from .. import data, helper
from p2pool.util import pack


P2P_PREFIX = 'fabfb5da'.decode('hex')
P2P_PORT = 5889
ADDRESS_VERSION = 71
ADDRESS_P2SH_VERSION = 5
RPC_PORT = 5888
RPC_CHECK = defer.inlineCallbacks(lambda bitcoind: defer.returnValue(
            (yield helper.check_block_header(bitcoind, '4d96a915f49d40b1e5c2844d1ee2dccb90013a990ccea12c492d22110489f0c4')) and # genesis block
            (yield helper.check_block_header(bitcoind, '34abd12dc4d9400b1ff049fe2605d22e2e7ae230f455152e4e2cd012fc3e45f7')) and # 208301 -- Lyra2RE fork
            (yield helper.check_block_header(bitcoind, '7c9c6fe9b3971c66e1ae7a27ac9fba96fb5a036fe50711038e43f9cd1901d8ab')) and # 347000 -- Lyra2REv2 fork
            (yield helper.check_block_header(bitcoind, '8d7585b3cd03c8911fb3b7bf82af530d0dc8730d4b670a5a695f9f2f16b7ad10')) and # 1080001 -- Lyra2REv3 fork
            (yield bitcoind.rpc_getblockchaininfo())['chain'] == 'main'
        ))
SUBSIDY_FUNC = lambda height: 50*100000000 >> (height + 1)//840000
POW_FUNC = lambda data: pack.IntType(256).unpack(__import__('lyra2re3_hash').getPoWHash(data))
BLOCK_PERIOD = 150 # s
SYMBOL = 'VTC'
CONF_FILE_FUNC = lambda: os.path.join(os.path.join(os.environ['APPDATA'], 'Vertcoin') if platform.system() == 'Windows' else os.path.expanduser('~/Library/Application Support/Vertcoin/') if platform.system() == 'Darwin' else os.path.expanduser('~/.vertcoin'), 'vertcoin.conf')
BLOCK_EXPLORER_URL_PREFIX = 'http://explorer.vtconline.org/block/'
ADDRESS_EXPLORER_URL_PREFIX = 'http://explorer.vtconline.org/address/'
TX_EXPLORER_URL_PREFIX = 'http://explorer.vtconline.org/tx/'
SANE_TARGET_RANGE = (2**256//1000000000000000000 - 1, 2**256//100000 - 1)
DUMB_SCRYPT_DIFF = 16
DUST_THRESHOLD = 0.03e8
HUMAN_READABLE_PART = 'vertcoin'
