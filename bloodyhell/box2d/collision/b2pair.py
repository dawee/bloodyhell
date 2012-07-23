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

from box2d.common.b2settings import *


class b2Pair(object):

    b2_nullPair = b2Settings.USHRT_MAX
    b2_nullProxy = b2Settings.USHRT_MAX
    b2_tableCapacity = b2Settings.b2_maxPairs
    b2_tableMask = b2_tableCapacity - 1
    e_pairBuffered = 0x0001
    e_pairRemoved = 0x0002
    e_pairFinal = 0x0004

    def __init__(self):
        self.userData = None
        self.proxyId1 = 0
        self.proxyId2 = 0
        self.next = 0
        self.status = 0

    def SetBuffered(self):
        self.status |= b2Pair.e_pairBuffered

    def ClearBuffered(self):
        self.status &= ~b2Pair.e_pairBuffered

    def IsBuffered(self):
        return (self.status & b2Pair.e_pairBuffered) == b2Pair.e_pairBuffered

    def SetRemoved(self):
        self.status |= b2Pair.e_pairRemoved

    def ClearRemoved(self):
        self.status &= ~b2Pair.e_pairRemoved

    def IsRemoved(self):
        return (self.status & b2Pair.e_pairRemoved) == b2Pair.e_pairRemoved

    def SetFinal(self):
        self.status |= b2Pair.e_pairFinal

    def IsFinal(self):
        return (self.status & b2Pair.e_pairFinal) == b2Pair.e_pairFinal
