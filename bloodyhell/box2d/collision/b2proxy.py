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

from box2d.collision.b2broadphase import b2BroadPhase

class b2Proxy(object):

    lowerBounds = [0, 0]
    upperBounds = [0, 0]
    overlapCount = 0
    timeStamp = 0
    userData = None

    def GetNext(self):
        return self.lowerBounds[0]

    def SetNext(self, next):
        self.lowerBounds[0] = next

    def IsValid(self):
        return self.overlapCount != b2BroadPhase.b2_invalid

