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
"""
This broad phase uses the Sweep and Prune algorithm in:
Collision Detection in Interactive 3D Environments by Gino van den Bergen
Also, some ideas, such integral values for fast compares comes from
Bullet (http:/www.bulletphysics.com).
"""

from box2d.common.b2settings import *


class b2BroadPhase(object):

    s_validate = False
    b2_invalid = b2Settings.USHRT_MAX
    b2_nullEdge = b2Settings.USHRT_MAX
    m_pairManager = b2PairManager()
    m_proxyPool = range(b2Settings.b2_maxPairs)
    m_freeProxy = 0
    m_bounds = range(2 * b2Settings.b2_maxProxies)
    m_queryResults = range(b2Settings.b2_maxProxies)
    m_queryResultCount = 0
    m_worldAABB = None
    m_quantizationFactor = b2Vec2()
    m_proxyCount = 0
    m_timeStamp = 0

    def __init__(self, worldAABB, callback):
        self.m_pairManager = b2PairManager()
        self.m_proxyPool = range(b2Settings.b2_maxPairs)
        self.m_bounds = range(2*b2Settings.b2_maxProxies)
        self.m_queryResults = range(b2Settings.b2_maxProxies)
        self.m_quantizationFactor = b2Vec2()
        i = 0
        self.m_pairManager.Initialize(self, callback)
        self.m_worldAABB = worldAABB
        self.m_proxyCount = 0
        for i in range(b2Settings.b2_maxProxies):
            self.m_queryResults[i] = 0
        self.m_bounds = range(2)
        for i in range(2):
            self.m_bounds[i] = range(2*b2Settings.b2_maxProxies)
        for j in range(2*b2Settings.b2_maxProxies):
            self.m_bounds[i][j] = b2Bound()
        dX = worldAABB.maxVertex.x
        dY = worldAABB.maxVertex.y
        dX -= worldAABB.minVertex.x
        dY -= worldAABB.minVertex.y
        self.m_quantizationFactor.x = b2Settings.USHRT_MAX / dX
        self.m_quantizationFactor.y = b2Settings.USHRT_MAX / dY
        tProxy
        for i in range(b2Settings.b2_maxProxies-1):
            tProxy = b2Proxy()
            self.m_proxyPool[i] = tProxy
            tProxy.SetNext(i + 1)
            tProxy.timeStamp = 0
            tProxy.overlapCount = b2BroadPhase.b2_invalid
            tProxy.userData = null
        tProxy = b2Proxy()
        self.m_proxyPool[b2Settings.b2_maxProxies-1] = tProxy
        tProxy.SetNext(b2Pair.b2_nullProxy)
        tProxy.timeStamp = 0
        tProxy.overlapCount = b2BroadPhase.b2_invalid
        tProxy.userData = null
        self.m_freeProxy = 0
        self.m_timeStamp = 1
        self.m_queryResultCount = 0

    def InRange(self,aabb):
        dX = aabb.minVertex.x
        dY = aabb.minVertex.y
        dX -= self.m_worldAABB.maxVertex.x
        dY -= self.m_worldAABB.maxVertex.y
        d2X = self.m_worldAABB.minVertex.x
        d2Y = self.m_worldAABB.minVertex.y
        d2X -= aabb.maxVertex.x
        d2Y -= aabb.maxVertex.y
        dX = b2Math.b2Max(dX, d2X)
        dY = b2Math.b2Max(dY, d2Y)
        return b2Math.b2Max(dX, dY) < 0.0

    def GetProxy(self,proxyId):
        if (proxyId == b2Pair.b2_nullProxy or self.m_proxyPool[proxyId].IsValid() == False):
            return null
        return self.m_proxyPool[ proxyId ]

    def CreateProxy(self,aabb, userData):
        index = 0
        proxy
        proxyId = self.m_freeProxy
        proxy = self.m_proxyPool[ proxyId ]
        self.m_freeProxy = proxy.GetNext()
        proxy.overlapCount = 0
        proxy.userData = userData
        boundCount = 2 * self.m_proxyCount
        lowerValues = range()
        upperValues = range()
        self.ComputeBounds(lowerValues, upperValues, aabb)
        for axis in range(2):
            bounds = self.m_bounds[axis]
            lowerIndex = 0
            upperIndex = 0
            lowerIndexOut = [lowerIndex]
            upperIndexOut = [upperIndex]
            self.Query(lowerIndexOut, upperIndexOut, lowerValues[axis], upperValues[axis], bounds, boundCount, axis)
            lowerIndex = lowerIndexOut[0]
            upperIndex = upperIndexOut[0]
            tArr = range()
            j = 0
            tEnd = boundCount - upperIndex
            tBound1
            tBound2
            for j in range(tEnd):
                tArr[j] = b2Bound()
                tBound1 = tArr[j]
                tBound2 = bounds[upperIndex+j]
                tBound1.value = tBound2.value
                tBound1.proxyId = tBound2.proxyId
                tBound1.stabbingCount = tBound2.stabbingCount
            tEnd = tArr.length
            tIndex = upperIndex+2
            for j in range(tEnd):
                tBound2 = tArr[j]
                tBound1 = bounds[tIndex+j]
                tBound1.value = tBound2.value
                tBound1.proxyId = tBound2.proxyId
                tBound1.stabbingCount = tBound2.stabbingCount
            tArr = range()
            tEnd = upperIndex - lowerIndex
            for j in range(tEnd):
                tArr[j] = b2Bound()
                tBound1 = tArr[j]
                tBound2 = bounds[lowerIndex+j]
                tBound1.value = tBound2.value
                tBound1.proxyId = tBound2.proxyId
                tBound1.stabbingCount = tBound2.stabbingCount
            tEnd = tArr.length
            tIndex = lowerIndex+1
            for j in range(tEnd):
                tBound2 = tArr[j]
                tBound1 = bounds[tIndex+j]
                tBound1.value = tBound2.value
                tBound1.proxyId = tBound2.proxyId
                tBound1.stabbingCount = tBound2.stabbingCount
            upperIndex += 1
            bounds[lowerIndex].value = lowerValues[axis]
            bounds[lowerIndex].proxyId = proxyId
            bounds[upperIndex].value = upperValues[axis]
            bounds[upperIndex].proxyId = proxyId
            bounds[lowerIndex].stabbingCount = 0 if lowerIndex == 0 else bounds[lowerIndex-1].stabbingCount
            bounds[upperIndex].stabbingCount = bounds[upperIndex-1].stabbingCount
            for index in range(upperIndex):
                bounds[index].stabbingCount += 1
            for index in range(boundCount+2):
                proxy2 = self.m_proxyPool[ bounds[index].proxyId ]
                if (bounds[index].IsLower()):
                    proxy2.lowerBounds[axis] = index
                else:
                    proxy2.upperBounds[axis] = index
            self.m_proxyCount += 1
        for i in range(self.m_queryResultCount):
            self.m_pairManager.AddBufferedPair(proxyId, self.m_queryResults[i])
        self.m_pairManager.Commit()
        self.m_queryResultCount = 0
        self.IncrementTimeStamp()
        return proxyId

    def DestroyProxy(self,proxyId):
        proxy = self.m_proxyPool[ proxyId ]
        boundCount = 2 * self.m_proxyCount
        for axis in range(2):
            bounds = self.m_bounds[axis]
            lowerIndex = proxy.lowerBounds[axis]
            upperIndex = proxy.upperBounds[axis]
            lowerValue = bounds[lowerIndex].value
            upperValue = bounds[upperIndex].value
            tArr = range()
            j = 0
            tEnd = upperIndex - lowerIndex - 1
            for j in range(tEnd):
                tArr[j] = b2Bound()
                tBound1 = tArr[j]
                tBound2 = bounds[lowerIndex+1+j]
                tBound1.value = tBound2.value
                tBound1.proxyId = tBound2.proxyId
                tBound1.stabbingCount = tBound2.stabbingCount
            tEnd = tArr.length
            tIndex = lowerIndex
            for j in range(tEnd):
                tBound2 = tArr[j]
                tBound1 = bounds[tIndex+j]
                tBound1.value = tBound2.value
                tBound1.proxyId = tBound2.proxyId
                tBound1.stabbingCount = tBound2.stabbingCount
            tArr = range()
            tEnd = boundCount - upperIndex - 1
            for j in range(tEnd):
                tArr[j] = b2Bound()
                tBound1 = tArr[j]
                tBound2 = bounds[upperIndex+1+j]
                tBound1.value = tBound2.value
                tBound1.proxyId = tBound2.proxyId
                tBound1.stabbingCount = tBound2.stabbingCount
            tEnd = tArr.length
            tIndex = upperIndex-1
            for j in range(tEnd):
                tBound2 = tArr[j]
                tBound1 = bounds[tIndex+j]
                tBound1.value = tBound2.value
                tBound1.proxyId = tBound2.proxyId
                tBound1.stabbingCount = tBound2.stabbingCount
            tEnd = boundCount - 2
            for index in range(tEnd):
                proxy2 = self.m_proxyPool[ bounds[index].proxyId ]
                if (bounds[index].IsLower()):
                    proxy2.lowerBounds[axis] = index
                else:
                    proxy2.upperBounds[axis] = index
            tEnd = upperIndex - 1
            for index2 in range(tEnd):
                bounds[index2].stabbingCount -= 1
            self.Query([0], [0], lowerValue, upperValue, bounds, boundCount - 2, axis)
        for i in range(self.m_queryResultCount):
            self.m_pairManager.RemoveBufferedPair(proxyId, self.m_queryResults[i])
        self.m_pairManager.Commit()
        self.m_queryResultCount = 0
        self.IncrementTimeStamp()
        proxy.userData = null
        proxy.overlapCount = b2BroadPhase.b2_invalid
        proxy.lowerBounds[0] = b2BroadPhase.b2_invalid
        proxy.lowerBounds[1] = b2BroadPhase.b2_invalid
        proxy.upperBounds[0] = b2BroadPhase.b2_invalid
        proxy.upperBounds[1] = b2BroadPhase.b2_invalid
        proxy.SetNext(self.m_freeProxy)
        self.m_freeProxy = proxyId
        self.m_proxyCount -= 1

    def MoveProxy(self,proxyId, aabb):
        axis = 0
        index = 0
        bound
        prevBound
        nextBound
        nextProxyId = 0
        nextProxy
        if (proxyId == b2Pair.b2_nullProxy or b2Settings.b2_maxProxies <= proxyId):
            return
        if (aabb.IsValid() == False):
            return
        boundCount = 2 * self.m_proxyCount
        proxy = self.m_proxyPool[ proxyId ]
        newValues = b2BoundValues()
        self.ComputeBounds(newValues.lowerValues, newValues.upperValues, aabb)
        oldValues = b2BoundValues()
        for axis in range(2):
            oldValues.lowerValues[axis] = self.m_bounds[axis][proxy.lowerBounds[axis]].value
            oldValues.upperValues[axis] = self.m_bounds[axis][proxy.upperBounds[axis]].value
        for axis in range(2):
            bounds = self.m_bounds[axis]
            lowerIndex = proxy.lowerBounds[axis]
            upperIndex = proxy.upperBounds[axis]
            lowerValue = newValues.lowerValues[axis]
            upperValue = newValues.upperValues[axis]
            deltaLower = lowerValue - bounds[lowerIndex].value
            deltaUpper = upperValue - bounds[upperIndex].value
            bounds[lowerIndex].value = lowerValue
            bounds[upperIndex].value = upperValue
            if (deltaLower < 0):
                index = lowerIndex
                while (index > 0 and lowerValue < bounds[index-1].value):
                    bound = bounds[index]
                    prevBound = bounds[index - 1]
                    prevProxyId = prevBound.proxyId
                    prevProxy = self.m_proxyPool[ prevBound.proxyId ]
                    prevBound.stabbingCount += 1
                    if (prevBound.IsUpper() == True):
                        if (self.TestOverlap(newValues, prevProxy)):
                            self.m_pairManager.AddBufferedPair(proxyId, prevProxyId)
                        prevProxy.upperBounds[axis] += 1
                        bound.stabbingCount += 1
                    else:
                        prevProxy.lowerBounds[axis] += 1
                        bound.stabbingCount -= 1
                    proxy.lowerBounds[axis] -= 1
                    bound.Swap(prevBound)
                    index -= 1
            if (deltaUpper > 0):
                index = upperIndex
                while (index < boundCount-1 and bounds[index+1].value <= upperValue):
                    bound = bounds[ index ]
                    nextBound = bounds[ index + 1 ]
                    nextProxyId = nextBound.proxyId
                    nextProxy = self.m_proxyPool[ nextProxyId ]
                    nextBound.stabbingCount += 1
                    if (nextBound.IsLower() == True):
                        if (self.TestOverlap(newValues, nextProxy)):
                            self.m_pairManager.AddBufferedPair(proxyId, nextProxyId)
                        nextProxy.lowerBounds[axis] -= 1
                        bound.stabbingCount += 1
                    else:
                        nextProxy.upperBounds[axis] -= 1
                        bound.stabbingCount -= 1
                    proxy.upperBounds[axis] += 1
                    bound.Swap(nextBound)
                    index += 1
            if (deltaLower > 0):
                index = lowerIndex
                while (index < boundCount-1 and bounds[index+1].value <= lowerValue):
                    bound = bounds[ index ]
                    nextBound = bounds[ index + 1 ]
                    nextProxyId = nextBound.proxyId
                    nextProxy = self.m_proxyPool[ nextProxyId ]
                    nextBound.stabbingCount -= 1
                    if (nextBound.IsUpper()):
                        if (self.TestOverlap(oldValues, nextProxy)):
                            self.m_pairManager.RemoveBufferedPair(proxyId, nextProxyId)
                        nextProxy.upperBounds[axis] -= 1
                        bound.stabbingCount -= 1
                    else:
                        nextProxy.lowerBounds[axis] -= 1
                        bound.stabbingCount += 1
                    proxy.lowerBounds[axis] += 1
                    bound.Swap(nextBound)
                    index += 1
            if (deltaUpper < 0):
                index = upperIndex
                while (index > 0 and upperValue < bounds[index-1].value):
                    bound = bounds[index]
                    prevBound = bounds[index - 1]
                    prevProxyId = prevBound.proxyId
                    prevProxy = self.m_proxyPool[ prevProxyId ]
                    prevBound.stabbingCount -= 1
                    if (prevBound.IsLower() == True):
                        if (self.TestOverlap(oldValues, prevProxy)):
                            self.m_pairManager.RemoveBufferedPair(proxyId, prevProxyId)
                        prevProxy.lowerBounds[axis] += 1
                        bound.stabbingCount -= 1
                    else:
                        prevProxy.upperBounds[axis] += 1
                        bound.stabbingCount += 1
                    proxy.upperBounds[axis] -= 1
                    bound.Swap(prevBound)
                    index -= 1

    def Commit(self):
        self.m_pairManager.Commit()

    def QueryAABB(self,aabb, userData, maxCount):
        lowerValues = range()
        upperValues = range()
        self.ComputeBounds(lowerValues, upperValues, aabb)
        lowerIndex = 0
        upperIndex = 0
        lowerIndexOut = [lowerIndex]
        upperIndexOut = [upperIndex]
        self.Query(lowerIndexOut, upperIndexOut, lowerValues[0], upperValues[0], self.m_bounds[0], 2*self.m_proxyCount, 0)
        self.Query(lowerIndexOut, upperIndexOut, lowerValues[1], upperValues[1], self.m_bounds[1], 2*self.m_proxyCount, 1)
        count = 0
        for i in range(self.m_queryResultCountandcount):
            proxy = self.m_proxyPool[ self.m_queryResults[i] ]
            userData[i] = proxy.userData
        self.m_queryResultCount = 0
        self.IncrementTimeStamp()
        return count

    def Validate(self):
        pair
        proxy1
        proxy2
        overlap
        for axis in range(2):
            bounds = self.m_bounds[axis]
            boundCount = 2 * self.m_proxyCount
            stabbingCount = 0
        for i in range(boundCount):
                bound = bounds[i]
                if (bound.IsLower() == True):
                    stabbingCount += 1
                else:
                    stabbingCount -= 1

    def ComputeBounds(self,lowerValues, upperValues, aabb):
        minVertexX = aabb.minVertex.x
        minVertexY = aabb.minVertex.y
        minVertexX = b2Math.b2Min(minVertexX, self.m_worldAABB.maxVertex.x)
        minVertexY = b2Math.b2Min(minVertexY, self.m_worldAABB.maxVertex.y)
        minVertexX = b2Math.b2Max(minVertexX, self.m_worldAABB.minVertex.x)
        minVertexY = b2Math.b2Max(minVertexY, self.m_worldAABB.minVertex.y)
        maxVertexX = aabb.maxVertex.x
        maxVertexY = aabb.maxVertex.y
        maxVertexX = b2Math.b2Min(maxVertexX, self.m_worldAABB.maxVertex.x)
        maxVertexY = b2Math.b2Min(maxVertexY, self.m_worldAABB.maxVertex.y)
        maxVertexX = b2Math.b2Max(maxVertexX, self.m_worldAABB.minVertex.x)
        maxVertexY = b2Math.b2Max(maxVertexY, self.m_worldAABB.minVertex.y)
        lowerValues[0] = """uint"""(self.m_quantizationFactor.x * (minVertexX - self.m_worldAABB.minVertex.x)) & (b2Settings.USHRT_MAX - 1)
        upperValues[0] = ("""uint"""(self.m_quantizationFactor.x * (maxVertexX - self.m_worldAABB.minVertex.x))& 0x0000ffff) | 1
        lowerValues[1] = """uint"""(self.m_quantizationFactor.y * (minVertexY - self.m_worldAABB.minVertex.y)) & (b2Settings.USHRT_MAX - 1)
        upperValues[1] = ("""uint"""(self.m_quantizationFactor.y * (maxVertexY - self.m_worldAABB.minVertex.y))& 0x0000ffff) | 1

    def TestOverlapValidate(self,p1, p2):
        for axis in range(2):
            bounds = self.m_bounds[axis]
            if (bounds[p1.lowerBounds[axis]].value > bounds[p2.upperBounds[axis]].value):
                return False
            if (bounds[p1.upperBounds[axis]].value < bounds[p2.lowerBounds[axis]].value):
                return False
        return True

    def TestOverlap(self,b, p):
        for axis in range(2):
            bounds = self.m_bounds[axis]
            if (b.lowerValues[axis] > bounds[p.upperBounds[axis]].value):
                return False
            if (b.upperValues[axis] < bounds[p.lowerBounds[axis]].value):
                return False
        return True

    def Query(self,lowerQueryOut, upperQueryOut, lowerValue, upperValue, bounds, boundCount, axis):
        lowerQuery = b2BroadPhase.BinarySearch(bounds, boundCount, lowerValue)
        upperQuery = b2BroadPhase.BinarySearch(bounds, boundCount, upperValue)
        for j in range(upperQuery):
            if (bounds[j].IsLower()):
                self.IncrementOverlapCount(bounds[j].proxyId)
        if (lowerQuery > 0):
            i = lowerQuery - 1
            s = bounds[i].stabbingCount
            while (s):
                if (bounds[i].IsLower()):
                    proxy = self.m_proxyPool[ bounds[i].proxyId ]
                    if (lowerQuery <= proxy.upperBounds[axis]):
                        self.IncrementOverlapCount(bounds[i].proxyId)
                        s -= 1
                i -= 1
        lowerQueryOut[0] = lowerQuery
        upperQueryOut[0] = upperQuery

    def IncrementOverlapCount(self,proxyId):
        proxy = self.m_proxyPool[ proxyId ]
        if (proxy.timeStamp < self.m_timeStamp):
            proxy.timeStamp = self.m_timeStamp
            proxy.overlapCount = 1
        else:
            proxy.overlapCount = 2
            self.m_queryResults[self.m_queryResultCount] = proxyId
            self.m_queryResultCount += 1

    def BinarySearch(self, bounds, count, value):
        low = 0
        high = count - 1
        while (low <= high):
            mid = int((low + high) / 2)
            if (bounds[mid].value > value):
                high = mid - 1
            elif (bounds[mid].value < value):
                low = mid + 1
            else:
                return (mid)
        return (low)

    def IncrementTimeStamp(self):
        if (self.m_timeStamp == b2Settings.USHRT_MAX):
            for i in range(b2Settings.b2_maxProxies):
                self.m_proxyPool[i].timeStamp = 0
            self.m_timeStamp = 1
        else:
            self.m_timeStamp += 1


