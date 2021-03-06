from plenum.client.client import Client
from plenum.test.eventually import eventually
from plenum.test.helper import checkSufficientRepliesRecvd, \
    sendRandomRequest


def testMerkleProofForFirstLeaf(client1: Client, replied1):
    replies = client1.getRepliesFromAllNodes(1).values()
    assert Client.verifyMerkleProof(*replies)


def testMerkleProofForNonFirstLeaf(looper, nodeSet, wallet1, client1, replied1):
    req2 = sendRandomRequest(wallet1, client1)
    f = nodeSet.f
    looper.run(eventually(checkSufficientRepliesRecvd, client1.inBox, req2.reqId
                          , f, retryWait=1, timeout=15))
    replies = client1.getRepliesFromAllNodes(req2.reqId).values()
    assert Client.verifyMerkleProof(*replies)
