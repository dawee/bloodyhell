"""
* Copyright (c) 2006-2007 Erin Catto http:
*
* This software is provided 'as-is', without any express or implied
* warranty.  In no event will the authors be held liable for any damages
* arising from the use of self software.
* Permission is granted to anyone to use self software for any purpose,
* including commercial applications, and to alter it and redistribute it
* freely, subject to the following restrictions:
* 1. The origin of self software must not be misrepresented you must not
* claim that you wrote the original software. If you use self software
* in a product, an acknowledgment in the product documentation would be
* appreciated but is not required.
* 2. Altered source versions must be plainly marked, and must not be
* misrepresented the original software.
* 3. This notice may not be removed or altered from any source distribution.
"""

from box2d.collision.b2pair import b2Pair
from box2d.collision.b2bufferedpair import b2BufferedPair
from box2d.common.b2settings import *


class b2PairManager(object):

    m_broadPhase = None
    m_callback = None
    m_pairs = None
    m_freePair = 0
    m_pairCount = 0
    m_pairBuffer = None
    m_pairBufferCount = 0
    m_hashTable = None

    def __init__(self):
        self.m_broadPhase = broadPhase
        self.m_callback = callback
        i = 0
        self.m_hashTable = range(b2Pair.b2_tableCapacity)
        for i in range(b2Pair.b2_tableCapacity):
            self.m_hashTable[i] = b2Pair.b2_nullPair
        self.m_pairs = range(b2Settings.b2_maxPairs)
        for i in range(b2Settings.b2_maxPairs):
            self.m_pairs[i] = b2Pair()
        self.m_pairBuffer = range(b2Settings.b2_maxPairs)
        for i in range(b2Settings.b2_maxPairs):
            self.m_pairBuffer[i] = b2BufferedPair()
        for i in range(b2Settings.b2_maxPairs):
            self.m_pairs[i].proxyId1 = b2Pair.b2_nullProxy
            self.m_pairs[i].proxyId2 = b2Pair.b2_nullProxy
            self.m_pairs[i].userData = null
            self.m_pairs[i].status = 0
            self.m_pairs[i].next = (i + 1)
        self.m_pairs[b2Settings.b2_maxPairs-1].next = b2Pair.b2_nullPair
        self.m_pairCount = 0

    """
    As proxies are created and moved, many pairs are created and destroyed. Even worse, the same
    pair may be added and removed multiple times in a single time step of the physics engine. To reduce
    traffic in the pair manager, we try to avoid destroying pairs in the pair manager until the
    end of the physics step. This is done by buffering all the self.RemovePair requests. self.AddPair
    requests are processed immediately because we need the hash table entry for quick lookup.
    All user user callbacks are delayed until the buffered pairs are confirmed in self.Commit.
    This is very important because the user callbacks may be very expensive and client logic
    may be harmed if pairs are added and removed within the same time step.
    Buffer a pair for addition.
    We may add a pair that is not in the pair manager or pair buffer.
    We may add a pair that is already in the pair manager and pair buffer.
    If the added pair is not a new pair, then it must be in the pair buffer (because self.RemovePair was called).
    """

    def AddBufferedPair(self,proxyId1, proxyId2):
        pair = self.AddPair(proxyId1, proxyId2)
        if (pair.IsBuffered() == false):
            pair.SetBuffered()
            self.m_pairBuffer[self.m_pairBufferCount].proxyId1 = pair.proxyId1
            self.m_pairBuffer[self.m_pairBufferCount].proxyId2 = pair.proxyId2
            self.m_pairBufferCount += 1
        pair.ClearRemoved()
        if (b2BroadPhase.s_validate):
            self.ValidateBuffer()

    def RemoveBufferedPair(self,proxyId1, proxyId2):
        pair = self.Find(proxyId1, proxyId2)
        if (pair == null):
            return
        if (pair.IsBuffered() == false):
            pair.SetBuffered()
            self.m_pairBuffer[self.m_pairBufferCount].proxyId1 = pair.proxyId1
            self.m_pairBuffer[self.m_pairBufferCount].proxyId2 = pair.proxyId2
            self.m_pairBufferCount += 1
        pair.SetRemoved()
        if (b2BroadPhase.s_validate):
            self.ValidateBuffer()

    def Commit(self):
        i = 0
        removeCount = 0
        proxies = self.m_broadPhase.m_proxyPool
        for i in range(self.m_pairBufferCount):
            pair = self.Find(self.m_pairBuffer[i].proxyId1, self.m_pairBuffer[i].proxyId2)
            pair.ClearBuffered()
            proxy1 = proxies[ pair.proxyId1 ]
            proxy2 = proxies[ pair.proxyId2 ]
            if (pair.IsRemoved()):
                if (pair.IsFinal() == true):
                    self.m_callback.PairRemoved(proxy1.userData, proxy2.userData, pair.userData)
                self.m_pairBuffer[removeCount].proxyId1 = pair.proxyId1
                self.m_pairBuffer[removeCount].proxyId2 = pair.proxyId2
                removeCount += 1
            else:
                if (pair.IsFinal() == false):
                    pair.userData = self.m_callback.PairAdded(proxy1.userData, proxy2.userData)
                    pair.SetFinal()
        for i in range(removeCount):
            self.RemovePair(self.m_pairBuffer[i].proxyId1, self.m_pairBuffer[i].proxyId2)
        self.m_pairBufferCount = 0
        if (b2BroadPhase.s_validate):
            self.ValidateTable()

    def AddPair(self,proxyId1, proxyId2):
        if (proxyId1 > proxyId2):
            temp = proxyId1
            proxyId1 = proxyId2
            proxyId2 = temp
        mHash = b2PairManager.Hash(proxyId1, proxyId2) & b2Pair.b2_tableMask
        pair = pair = self.FindHash(proxyId1, proxyId2, mHash)
        if (pair != null):
            return pair
        pIndex = self.m_freePair
        pair = self.m_pairs[pIndex]
        self.m_freePair = pair.next
        pair.proxyId1 = proxyId1
        pair.proxyId2 = proxyId2
        pair.status = 0
        pair.userData = null
        pair.next = self.m_hashTable[mHash]
        self.m_hashTable[mHash] = pIndex
        ++self.m_pairCount
        return pair

    def RemovePair(self,proxyId1, proxyId2):
        if (proxyId1 > proxyId2):
            temp = proxyId1
            proxyId1 = proxyId2
            proxyId2 = temp
        mHash = b2PairManager.Hash(proxyId1, proxyId2) & b2Pair.b2_tableMask
        node = self.m_hashTable[mHash]
        pNode = null
        while (node != b2Pair.b2_nullPair):
            if (b2PairManager.Equals(self.m_pairs[node], proxyId1, proxyId2)):
                index = node
                if (pNode):
                    pNode.next = self.m_pairs[node].next
                else:
                    self.m_hashTable[mHash] = self.m_pairs[node].next
                pair = self.m_pairs[ index ]
                userData = pair.userData
                pair.next = self.m_freePair
                pair.proxyId1 = b2Pair.b2_nullProxy
                pair.proxyId2 = b2Pair.b2_nullProxy
                pair.userData = null
                pair.status = 0
                self.m_freePair = index
                --self.m_pairCount
                return userData
            else:
                pNode = self.m_pairs[node]
                node = pNode.next
        return null

    def Find(self,proxyId1, proxyId2):
        if (proxyId1 > proxyId2):
            temp = proxyId1
            proxyId1 = proxyId2
            proxyId2 = temp
        mHash = b2PairManager.Hash(proxyId1, proxyId2) & b2Pair.b2_tableMask
        return self.FindHash(proxyId1, proxyId2, mHash)

    def FindHash(self,proxyId1, proxyId2, hash):
        index = self.m_hashTable[hash]
        while( index != b2Pair.b2_nullPair and b2PairManager.Equals(self.m_pairs[index], proxyId1, proxyId2) == false):
            index = self.m_pairs[index].next
        if ( index == b2Pair.b2_nullPair ):
            return null
        return self.m_pairs[ index ]

    def ValidateBuffer(self):
        pass

    def ValidateTable(self):
        pass

    @staticmethod
    def Hash(proxyId1, proxyId2):
        key = ((proxyId2 << 16) & 0xffff0000) | proxyId1
        key = ~key + ((key << 15) & 0xFFFF8000)
        key = key ^ ((key >> 12) & 0x000fffff)
        key = key + ((key << 2) & 0xFFFFFFFC)
        key = key ^ ((key >> 4) & 0x0fffffff)
        key = key * 2057
        key = key ^ ((key >> 16) & 0x0000ffff)
        return key

    def Equals(pair, proxyId1, proxyId2):
        return (pair.proxyId1 == proxyId1 and pair.proxyId2 == proxyId2)

    def EqualsPair(pair1, pair2):
        return pair1.proxyId1 == pair2.proxyId1 and pair1.proxyId2 == pair2.proxyId2
