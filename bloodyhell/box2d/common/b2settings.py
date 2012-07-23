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

import math


class b2Settings(object):

    USHRT_MAX = 0x0000ffff
    b2_pi = math.pi
    b2_massUnitsPerKilogram = 1.0
    b2_timeUnitsPerSecond = 1.0
    b2_lengthUnitsPerMeter = 30.0
    b2_maxManifoldPoints = 2
    b2_maxShapesPerBody = 64
    b2_maxPolyVertices = 8
    b2_maxProxies = 1024
    b2_maxPairs = 8 *     b2_maxProxies
    b2_linearSlop = 0.005 *     b2_lengthUnitsPerMeter
    b2_angularSlop = 2.0 / 180.0 *     b2_pi
    b2_velocityThreshold = 1.0 *     b2_lengthUnitsPerMeter /     b2_timeUnitsPerSecond
    b2_maxLinearCorrection = 0.2 *     b2_lengthUnitsPerMeter
    b2_maxAngularCorrection = 8.0 / 180.0 *     b2_pi
    b2_contactBaumgarte = 0.2
    b2_timeToSleep = 0.5 *     b2_timeUnitsPerSecond
    b2_linearSleepTolerance = 0.01 *     b2_lengthUnitsPerMeter /     b2_timeUnitsPerSecond
    b2_angularSleepTolerance = 2.0 / 180.0 /     b2_timeUnitsPerSecond

    @staticmethod
    def b2Assert(a):
        """
        if not a:
            nullVec
            nullVec.x++
        """
