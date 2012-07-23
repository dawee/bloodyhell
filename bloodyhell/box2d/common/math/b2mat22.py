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

from box2d.common.math.b2vec2 import b2Vec2


class b2Mat22(object):

    def __init__(self,angle=None, c1=None, c2=None):
        if (angle is None):
            angle = 0
        self.col1 = b2Vec2()
        self.col2 = b2Vec2()
        if (c1 is not None and c2 is not None):
            self.col1.SetV(c1)
            self.col2.SetV(c2)
        else:
            c = math.cos(angle)
            s = math.sin(angle)
            self.col1.x = c
            self.col2.x = -s
            self.col1.y = s
            self.col2.y = c

    def Set(self,angle):
        c = math.cos(angle)
        s = math.sin(angle)
        self.col1.x = c
        self.col2.x = -s
        self.col1.y = s
        self.col2.y = c

    def SetVV(self,c1, c2):
        self.col1.SetV(c1)
        self.col2.SetV(c2)

    def Copy(self):
        return b2Mat22(0, self.col1, self.col2)

    def SetM(self,m):
        self.col1.SetV(m.col1)
        self.col2.SetV(m.col2)

    def AddM(self,m):
        self.col1.x += m.col1.x
        self.col1.y += m.col1.y
        self.col2.x += m.col2.x
        self.col2.y += m.col2.y

    def SetIdentity(self):
        self.col1.x = 1.0
        self.col2.x = 0.0
        self.col1.y = 0.0
        self.col2.y = 1.0

    def SetZero(self):
        self.col1.x = 0.0
        self.col2.x = 0.0
        self.col1.y = 0.0
        self.col2.y = 0.0

    def Invert(self,out):
        a = self.col1.x
        b = self.col2.x
        c = self.col1.y
        d = self.col2.y
        det = a * d - b * c
        det = 1.0 / det
        out.col1.x =  det * d
        out.col2.x = -det * b
        out.col1.y = -det * c
        out.col2.y =  det * a
        return out

    def Solve(self,out, bX, bY):
        a11 = self.col1.x
        a12 = self.col2.x
        a21 = self.col1.y
        a22 = self.col2.y
        det = a11 * a22 - a12 * a21
        det = 1.0 / det
        out.x = det * (a22 * bX - a12 * bY)
        out.y = det * (a11 * bY - a21 * bX)
        return out

    def Abs(self):
        self.col1.Abs()
        self.col2.Abs()
