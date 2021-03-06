import logging

import pytest
from plenum.common.log import getlogger

from plenum.server.suspicion_codes import Suspicions
from plenum.test.eventually import eventually
from plenum.test.helper import TestNodeSet, checkNodesConnected, ensureElectionsDone, \
    delayerMsgTuple, whitelistNode

from plenum.common.types import Nomination
from plenum.server.replica import Replica
from plenum.test.primary_election.helpers import checkNomination, \
    getSelfNominationByNode

nodeCount = 4
whitelist = ['already got nomination',
             'doing nothing for now']

logger = getlogger()


@pytest.fixture()
def case1Setup(startedNodes: TestNodeSet):
    nodes = startedNodes
    nodeNames = nodes.nodeNames

    nodeB = nodes.getNode(nodeNames[1])

    # Node B delays self nomination so A's nomination reaches everyone
    nodeB.delaySelfNomination(10)
    # Node B delays nomination from all nodes
    nodeB.nodeIbStasher.delay(delayerMsgTuple(5, Nomination))

    # Add node C and node D
    nodeC = nodes.getNode(nodeNames[2])
    nodeD = nodes.getNode(nodeNames[3])

    # Node C should not try to nominate itself until it gets NOMINATE from B
    nodeC.delaySelfNomination(10)

    # Node D should delay its self nomination for long as it is a slow node
    # and should never win the
    # primary election even if a node maliciously tries to make Node D primary
    nodeD.delaySelfNomination(30)

    # A, C and D should not blacklist B since we are trying to check if
    # multiple nominations from the same node have any impact on
    # the election
    whitelistNode(nodeB.name,
                  [node for node in nodes if node != nodeB],
                  Suspicions.DUPLICATE_NOM_SENT.code)

    return nodes


# noinspection PyIncorrectDocstring
def testPrimaryElectionCase1(case1Setup, looper, keySharedNodes):
    """
    Case 1 - A node making multiple nominations for a particular node. Consider
    4 nodes A, B, C and D. Lets say node B is malicious and is repeatedly
    nominating Node D
    """
    nodes = keySharedNodes
    nodeA, nodeB, nodeC, nodeD = [nodes.getNode(nm) for nm in nodes.nodeNames]

    # Doesn't matter if nodes reach the ready state or not. Just start them
    looper.run(checkNodesConnected(nodes))

    # Node B sends multiple NOMINATE msgs for Node D but only after A has
    # nominated itself
    looper.run(eventually(checkNomination, nodeA, nodeA.name, retryWait=.25,
                          timeout=1))

    instId = getSelfNominationByNode(nodeA)

    for i in range(5):
        nodeB.send(Nomination(nodeD.name, instId, nodeB.viewNo))
    nodeB.nodestack.flushOutBoxes()

    # No node from node A, node C, node D(node B is malicious anyway so not
    # considering it) should have more than one nomination for node D since
    # node D is slow. The one nomination for D, that nodes A, C
    # and D might have would be because of node B
    for node in [nodeA, nodeC, nodeD]:
        assert list(node.elector.nominations[instId].values()).count(
            Replica.generateName(nodeD.name, instId)) \
               <= 1

    primaryReplicas = ensureElectionsDone(looper=looper, nodes=nodes,
                                          retryWait=1, timeout=30)

    for node in nodes:
        logger.debug(
            "{}'s nominations {}".format(node, node.elector.nominations))
    # Node D should not have any primary
    assert not nodeD.hasPrimary
    # A node other than Node D should not have any replica among the
    # primary replicas
    assert nodeD.name not in [pr.name for pr in primaryReplicas]
