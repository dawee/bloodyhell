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
            pass
