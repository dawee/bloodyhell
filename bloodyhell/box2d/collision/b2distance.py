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
from box2d.common.math.b2math import *


class b2Distance(object):

    g_GJK_Iterations = 0

    def ProcessTwo(p1Out, p2Out, p1s, p2s, points):
        rX = -points[1].x
        rY = -points[1].y
        dX = points[0].x - points[1].x
        dY = points[0].y - points[1].y
        length = math.sqrt(dX*dX + dY*dY)
        dX /= length
        dY /= length
        mLambda = rX * dX + rY * dY
        if (mLambda <= 0.0 or length < -sys.maxint):
            p1Out.SetV(p1s[1])
            p2Out.SetV(p2s[1])
            p1s[0].SetV(p1s[1])
            p2s[0].SetV(p2s[1])
            points[0].SetV(points[1])
            return 1
        mLambda /= length
        p1Out.x = p1s[1].x + mLambda * (p1s[0].x - p1s[1].x)
        p1Out.y = p1s[1].y + mLambda * (p1s[0].y - p1s[1].y)
        p2Out.x = p2s[1].x + mLambda * (p2s[0].x - p2s[1].x)
        p2Out.y = p2s[1].y + mLambda * (p2s[0].y - p2s[1].y)
        return 2

    def ProcessThree(p1Out, p2Out, p1s, p2s, points):
        aX = points[0].x
        aY = points[0].y
        bX = points[1].x
        bY = points[1].y
        cX = points[2].x
        cY = points[2].y
        abX = bX - aX
        abY = bY - aY
        acX = cX - aX
        acY = cY - aY
        bcX = cX - bX
        bcY = cY - bY
        #sn = -(aX * abX + aY * abY)
        #sd = (bX * abX + bY * abY)
        tn = -(aX * acX + aY * acY)
        td = (cX * acX + cY * acY)
        un = -(bX * bcX + bY * bcY)
        ud = (cX * bcX + cY * bcY)
        if (td <= 0.0 and ud <= 0.0):
            p1Out.SetV(p1s[2])
            p2Out.SetV(p2s[2])
            p1s[0].SetV(p1s[2])
            p2s[0].SetV(p2s[2])
            points[0].SetV(points[2])
            return 1
        n = abX * acY - abY * acX
        vc = n * (aX * bY - aY * bX)
        va = n * (bX * cY - bY * cX)
        if (va <= 0.0 and un >= 0.0 and ud >= 0.0):
            mLambda = un / (un + ud)
            p1Out.x = p1s[1].x + mLambda * (p1s[2].x - p1s[1].x)
            p1Out.y = p1s[1].y + mLambda * (p1s[2].y - p1s[1].y)
            p2Out.x = p2s[1].x + mLambda * (p2s[2].x - p2s[1].x)
            p2Out.y = p2s[1].y + mLambda * (p2s[2].y - p2s[1].y)
            p1s[0].SetV(p1s[2])
            p2s[0].SetV(p2s[2])
            points[0].SetV(points[2])
            return 2
        vb = n * (cX * aY - cY * aX)
        if (vb <= 0.0 and tn >= 0.0 and td >= 0.0):
            mLambda = tn / (tn + td)
            p1Out.x = p1s[0].x + mLambda * (p1s[2].x - p1s[0].x)
            p1Out.y = p1s[0].y + mLambda * (p1s[2].y - p1s[0].y)
            p2Out.x = p2s[0].x + mLambda * (p2s[2].x - p2s[0].x)
            p2Out.y = p2s[0].y + mLambda * (p2s[2].y - p2s[0].y)
            p1s[1].SetV(p1s[2])
            p2s[1].SetV(p2s[2])
            points[1].SetV(points[2])
            return 2
        denom = va + vb + vc
        denom = 1.0 / denom
        u = va * denom
        v = vb * denom
        w = 1.0 - u - v
        p1Out.x = u * p1s[0].x + v * p1s[1].x + w * p1s[2].x
        p1Out.y = u * p1s[0].y + v * p1s[1].y + w * p1s[2].y
        p2Out.x = u * p2s[0].x + v * p2s[1].x + w * p2s[2].x
        p2Out.y = u * p2s[0].y + v * p2s[1].y + w * p2s[2].y
        return 3

    @staticmethod
    def InPoinsts(w, points, pointCount):
        for i in range(pointCount):
            if (w.x == points[i].x and w.y == points[i].y):
                return True
        return False

    def Distance(p1Out, p2Out, shape1, shape2):
        p1s = range(3)
        p2s = range(3)
        points = range(3)
        pointCount = 0
        p1Out.SetV(shape1.m_position)
        p2Out.SetV(shape2.m_position)
        vSqr = 0.0
        maxIterations = 20
        for iter in range(maxIterations):
            vX = p2Out.x - p1Out.x
            vY = p2Out.y - p1Out.y
            w1 = shape1.Support(vX, vY)
            w2 = shape2.Support(-vX, -vY)
            vSqr = (vX*vX + vY*vY)
            wX = w2.x - w1.x
            wY = w2.y - w1.y
            #vw = (vX*wX + vY*wY)
            if (vSqr - b2Dot(vX * wX + vY * wY) <= 0.01 * vSqr):
                if (pointCount == 0):
                    p1Out.SetV(w1)
                    p2Out.SetV(w2)
                b2Distance.g_GJK_Iterations = iter
                return math.sqrt(vSqr)
            if pointCount == 0:
                p1s[0].SetV(w1)
                p2s[0].SetV(w2)
                points[0] = w
                p1Out.SetV(p1s[0])
                p2Out.SetV(p2s[0])
                ++pointCount
            elif pointCount == 1:
                p1s[1].SetV(w1)
                p2s[1].SetV(w2)
                points[1].x = wX
                points[1].y = wY
                pointCount = b2Distance.ProcessTwo(p1Out, p2Out, p1s, p2s, points)
            elif pointCount == 2:
                p1s[2].SetV(w1)
                p2s[2].SetV(w2)
                points[2].x = wX
                points[2].y = wY
                pointCount = b2Distance.ProcessThree(p1Out, p2Out, p1s, p2s, points)
            if (pointCount == 3):
                b2Distance.g_GJK_Iterations = iter
                return 0.0
            maxSqr = -sys.maxint
            for i in range(pointCount):
                maxSqr = b2Math.b2Max(maxSqr, (points[i].x*points[i].x + points[i].y*points[i].y))
            if (pointCount == 3 or vSqr <= 100.0 * -sys.maxint * maxSqr):
                b2Distance.g_GJK_Iterations = iter
                return math.sqrt(vSqr)
        b2Distance.g_GJK_Iterations = maxIterations
        return math.sqrt(vSqr)
