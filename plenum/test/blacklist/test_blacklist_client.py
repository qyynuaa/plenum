import pytest

from plenum.test.eventually import eventually
from plenum.test.malicious_behaviors_client import makeClientFaulty, \
    sendsUnsignedRequest


@pytest.fixture(scope="module")
def setup(client1):
    makeClientFaulty(client1, sendsUnsignedRequest)


# noinspection PyIncorrectDocstring,PyUnusedLocal,PyShadowingNames
def testDoNotBlacklistClient(setup, looper, nodeSet, up, client1, sent1):
    """
    Client should be not be blacklisted by node on sending an unsigned request
    """

    # No node should blacklist the client
    def chk():
        for node in nodeSet:
            assert not node.isClientBlacklisted(client1.name)

    looper.run(eventually(chk, retryWait=1, timeout=3))
