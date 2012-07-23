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

import sys
import math

from box2d.common.math.b2mat22 import b2Mat22
from box2d.common.math.b2vec2 import b2Vec2
from box2d.common.b2settings import b2Settings
from box2d.collision.b2distance import b2Distance

FLT_EPSILON = 1.192092896e-07


class b2Conservative(object):

    R1 = b2Mat22()
    R2 = b2Mat22()
    x1 = b2Vec2()
    x2 = b2Vec2()

    @staticmethod
    def Conservative(shape1, shape2):
        body1 = shape1.GetBody()
        body2 = shape2.GetBody()
        v1X = body1.m_position.x - body1.m_position0.x
        v1Y = body1.m_position.y - body1.m_position0.y
        omega1 = body1.m_rotation - body1.m_rotation0
        v2X = body2.m_position.x - body2.m_position0.x
        v2Y = body2.m_position.y - body2.m_position0.y
        omega2 = body2.m_rotation - body2.m_rotation0
        r1 = shape1.GetMaxRadius()
        r2 = shape2.GetMaxRadius()
        p1StartX = body1.m_position0.x
        p1StartY = body1.m_position0.y
        a1Start = body1.m_rotation0
        p2StartX = body2.m_position0.x
        p2StartY = body2.m_position0.y
        a2Start = body2.m_rotation0

        p1X = p1StartX
        p1Y = p1StartY
        a1 = a1Start
        p2X = p2StartX
        p2Y = p2StartY
        a2 = a2Start
        b2Conservative.R1.Set(a1)
        b2Conservative.R2.Set(a2)
        #shape1.QuickSync(p1, b2Conservative.R1)
        #shape2.QuickSync(p2, b2Conservative.R2)
        s1 = 0.0
        maxIterations = 10
        invRelativeVelocity = 0.0
        hit = True
        for iter in range(maxIterations):
            distance = b2Distance.Distance(b2Conservative.x1, b2Conservative.x2, shape1, shape2)
            if (distance < b2Settings.b2_linearSlop):
                if (iter == 0):
                    hit = False
                else:
                    hit = True
                break
            if (iter == 0):
                dX = b2Conservative.x2.x - b2Conservative.x1.x
                dY = b2Conservative.x2.y - b2Conservative.x1.y
                # dLen = math.sqrt(dX*dX + dY*dY)
                relativeVelocity = (dX*(v1X-v2X) + dY*(v1Y - v2Y)) + abs(omega1) * r1 + abs(omega2) * r2
                if (abs(relativeVelocity) < -sys.maxint):
                    hit = False
                    break
                invRelativeVelocity = 1.0 / relativeVelocity
            ds = distance * invRelativeVelocity
            s2 = s1 + ds
            if (s2 < 0.0 or 1.0 < s2):
                hit = False
                break
            if (s2 < (1.0 + 100.0 * -sys.maxint) * s1):
                hit = True
                break
            s1 = s2
            #p1X = p1StartX + s1 * v1.x
            #p1Y = p1StartY + s1 * v1.y
            a1 = a1Start + s1 * omega1
            #p2X = p2StartX + s1 * v2.x
            #p2Y = p2StartY + s1 * v2.y
            a2 = a2Start + s1 * omega2
            b2Conservative.R1.Set(a1)
            b2Conservative.R2.Set(a2)
            #shape1.QuickSync(p1, b2Conservative.R1)
            #shape2.QuickSync(p2, b2Conservative.R2)
        if (hit):
            dX = b2Conservative.x2.x - b2Conservative.x1.x
            dY = b2Conservative.x2.y - b2Conservative.x1.y
            length = math.sqrt(dX*dX + dY*dY)
            if (length > FLT_EPSILON):
                """
                d *= b2Settings.b2_linearSlop / length
                """
            if (body1.IsStatic()):
                body1.m_position.x = p1X
                body1.m_position.y = p1Y
            else:
                body1.m_position.x = p1X - dX
                body1.m_position.y = p1Y - dY
            body1.m_rotation = a1
            body1.m_R.Set(a1)
            body1.QuickSyncShapes()
            if (body2.IsStatic()):
                body2.m_position.x = p2X
                body2.m_position.y = p2Y
            else:
                body2.m_position.x = p2X + dX
                body2.m_position.y = p2Y + dY
            body2.m_position.x = p2X + dX
            body2.m_position.y = p2Y + dY
            body2.m_rotation = a2
            body2.m_R.Set(a2)
            body2.QuickSyncShapes()
            return True
        shape1.QuickSync(body1.m_position, body1.m_R)
        shape2.QuickSync(body2.m_position, body2.m_R)
        return False
