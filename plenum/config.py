from collections import OrderedDict

# Each entry in registry is (stack name, ((host, port), verkey, pubkey))

from plenum.common.txn import ClientBootStrategy
from plenum.common.types import PLUGIN_TYPE_STATS_CONSUMER, PLUGIN_BASE_DIR_PATH

nodeReg = OrderedDict([
    ('Alpha', ('127.0.0.1', 9701)),
    ('Beta', ('127.0.0.1', 9703)),
    ('Gamma', ('127.0.0.1', 9705)),
    ('Delta', ('127.0.0.1', 9707))
])

cliNodeReg = OrderedDict([
    ('AlphaC', ('127.0.0.1', 9702)),
    ('BetaC', ('127.0.0.1', 9704)),
    ('GammaC', ('127.0.0.1', 9706)),
    ('DeltaC', ('127.0.0.1', 9708))
])

baseDir = "~/.plenum/"

nodeDataDir = "data/nodes"

clientDataDir = "data/clients"

domainTransactionsFile = "transactions_sandbox"

poolTransactionsFile = "pool_transactions_sandbox"

walletDir = "wallet"

clientBootStrategy = ClientBootStrategy.PoolTxn

hashStore = {
    "type": "file"
}

primaryStorage = None

secondaryStorage = None

OrientDB = {
    "user": "root",
    "password": "password",
    "host": "127.0.0.1",
    "port": 2424
}

DefaultPluginPath = {
    # PLUGIN_BASE_DIR_PATH: "<abs path of plugin directory can be given here,
    #  if not given, by default it will pickup plenum/server/plugin path>",
    PLUGIN_TYPE_STATS_CONSUMER: "stats_consumer"
}

PluginsDir = "plugins"

stewardThreshold = 20

# Monitoring configuration
PerfCheckFreq = 10
DELTA = 0.8
LAMBDA = 60
OMEGA = 5
SendMonitorStats = True
ThroughputWindowSize = 30
DashboardUpdateFreq = 5
ThroughputGraphDuration = 240
LatencyWindowSize = 30
LatencyGraphDuration = 240

# Stats server configuration
STATS_SERVER_IP = '127.0.0.1'
STATS_SERVER_PORT = 50000

RAETLogLevel = "terse"
RAETLogLevelCli = "mute"
RAETLogFilePath = None
RAETLogFilePathCli = None
RAETMessageTimeout = 60


ViewChangeWindowSize = 60

# Timeout factor after which a node starts requesting consistency proofs if has
# not found enough matching
ConsistencyProofsTimeout = 5

# Timeout factor after which a node starts requesting transactions
CatchupTransactionsTimeout = 5

# Log configuration
logRotationWhen = 'D'
logRotationInterval = 1
logRotationBackupCount = 10
logFormat = '{asctime:s} | {levelname:8s} | {filename:20s} ({lineno:d}) | {funcName:s} | {message:s}'
logFormatStyle='{'


# OPTIONS RELATED TO TESTS

# Expected time for one stack to get connected to another
ExpectedConnectTime = 1.1
