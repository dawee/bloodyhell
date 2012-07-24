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


class b2Bound(object):

    def __init__(self):
        self.value = 0
        self.proxyId = 0
        self.stabbingCount = 0

    def IsLower(self):
        return (self.value & 1) == 0

    def IsUpper(self):
        return (self.value & 1) == 1

    def Swap(self, b):
        tempValue = self.value
        tempProxyId = self.proxyId
        tempStabbingCount = self.stabbingCount
        self.value = b.value
        self.proxyId = b.proxyId
        self.stabbingCount = b.stabbingCount
        b.value = tempValue
        b.proxyId = tempProxyId
        b.stabbingCount = tempStabbingCount
