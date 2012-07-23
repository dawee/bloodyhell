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

class b2Vec2(object):

    def __init__(self,x_=0.0, y_=0.0):
        self.x=x_
        self.y=y_

    def SetZero(self):
        self.x = 0.0
        self.y = 0.0

    def Set(self, x_, y_):
        self.x=x_
        self.y=y_

    def SetV(self, v):
        self.x=v.x
        self.y=v.y

    def Negative(self):
        return b2Vec2(-self.x, -self.y)

    def Copy(self):
        return b2Vec2(self.x,self.y)

    def Add(self,v):
        self.x += v.x
        self.y += v.y

    def Subtract(self,v):
        self.x -= v.x
        self.y -= v.y

    def Multiply(self,a):
        self.x *= a
        self.y *= a

    def MulM(self,A):
        tX = self.x
        self.x = A.col1.x * tX + A.col2.x * self.y
        self.y = A.col1.y * tX + A.col2.y * self.y

    def MulTM(self,A):
        from box2d.common.math.b2math import b2Math
        tX = b2Math.b2Dot(self, A.col1)
        self.y = b2Math.b2Dot(self, A.col2)
        self.x = tX

    def CrossVF(self,s):
        tX = self.x
        self.x = s * self.y
        self.y = -s * tX

    def CrossFV(self,s):
        tX = self.x
        self.x = -s * self.y
        self.y = s * tX

    def MinV(self,b):
        self.x = self.x if self.x < b.x else b.x
        self.y = self.y if self.y < b.y else b.y

    def MaxV(self,b):
        self.x = self.x if self.x > b.x else b.x
        self.y = self.y if self.y > b.y else b.y

    def Abs(self):
        self.x = abs(self.x)
        self.y = abs(self.y)

    def Length(self):
        return math.sqrt(self.x * self.x + self.y * self.y)

    def Normalize(self):
        length = self.Length()
        if (length < -sys.maxint):
            return 0.0
        invLength = 1.0 / length
        self.x *= invLength
        self.y *= invLength
        return length

    def IsValid(self):
        from box2d.common.math.b2math import b2Math
        return b2Math.b2IsValid(self.x) and b2Math.b2IsValid(self.y)

    @staticmethod
    def Make(x_, y_):
        return b2Vec2(x_, y_)
