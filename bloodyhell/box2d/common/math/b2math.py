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

import random

from box2d.common.math.b2vec2 import b2Vec2
from box2d.common.math.b2mat22 import b2Mat22


class b2Math(object):

    tempVec2 = b2Vec2()
    tempVec3 = b2Vec2()
    tempVec4 = b2Vec2()
    tempVec5 = b2Vec2()
    tempMat = b2Mat22()

    @staticmethod
    def b2IsValid(x):
        #return isFinite(x)
        return True

    @staticmethod
    def b2Dot(a, b):
        return a.x * b.x + a.y * b.y

    @staticmethod
    def b2CrossVV(a, b):
        return a.x * b.y - a.y * b.x

    @staticmethod
    def b2CrossVF(a, s):
        v = b2Vec2(s * a.y, -s * a.x)
        return v

    @staticmethod
    def b2CrossFV(s, a):
        v = b2Vec2(-s * a.y, s * a.x)
        return v

    @staticmethod
    def b2MulMV(A, v):
        u = b2Vec2(A.col1.x * v.x + A.col2.x * v.y, A.col1.y * v.x + A.col2.y * v.y)
        return u

    @staticmethod
    def b2MulTMV(A, v):
        u = b2Vec2(b2Math.b2Dot(v, A.col1), b2Math.b2Dot(v, A.col2))
        return u

    @staticmethod
    def AddVV(a, b):
        v = b2Vec2(a.x + b.x, a.y + b.y)
        return v

    @staticmethod
    def SubtractVV(a, b):
        v = b2Vec2(a.x - b.x, a.y - b.y)
        return v

    @staticmethod
    def MulFV(s, a):
        v = b2Vec2(s * a.x, s * a.y)
        return v

    @staticmethod
    def AddMM(A, B):
        C = b2Mat22(0, b2Math.AddVV(A.col1, B.col1), b2Math.AddVV(A.col2, B.col2))
        return C

    @staticmethod
    def b2MulMM(A, B):
        C = b2Mat22(0, b2Math.b2MulMV(A, B.col1), b2Math.b2MulMV(A, B.col2))
        return C

    @staticmethod
    def b2MulTMM(A, B):
        c1 = b2Vec2(b2Math.b2Dot(A.col1, B.col1), b2Math.b2Dot(A.col2, B.col1))
        c2 = b2Vec2(b2Math.b2Dot(A.col1, B.col2), b2Math.b2Dot(A.col2, B.col2))
        C = b2Mat22(0, c1, c2)
        return C

    @staticmethod
    def b2Abs(a):
        return a if a > 0.0 else -a

    @staticmethod
    def b2AbsV(a):
        b = b2Vec2(b2Math.b2Abs(a.x), b2Math.b2Abs(a.y))
        return b

    @staticmethod
    def b2AbsM(A):
        B = b2Mat22(0, b2Math.b2AbsV(A.col1), b2Math.b2AbsV(A.col2))
        return B

    @staticmethod
    def b2Min(a, b):
        return a if a < b else b

    @staticmethod
    def b2MinV(a, b):
        c = b2Vec2(b2Math.b2Min(a.x, b.x), b2Math.b2Min(a.y, b.y))
        return c

    @staticmethod
    def b2Max(a, b):
        return a if a > b else b

    @staticmethod
    def b2MaxV(a, b):
        c = b2Vec2(b2Math.b2Max(a.x, b.x), b2Math.b2Max(a.y, b.y))
        return c

    @staticmethod
    def b2Clamp(a, low, high):
        return b2Math.b2Max(low, b2Math.b2Min(a, high))

    @staticmethod
    def b2ClampV(a, low, high):
        return b2Math.b2MaxV(low, b2Math.b2MinV(a, high))

    @staticmethod
    def b2Swap(a, b):
        tmp = a[0]
        a[0] = b[0]
        b[0] = tmp

    @staticmethod
    def b2Random():
        return random.random() * 2 - 1

    @staticmethod
    def b2NextPowerOfTwo(x):
        x |= (x >> 1) & 0x7FFFFFFF
        x |= (x >> 2) & 0x3FFFFFFF
        x |= (x >> 4) & 0x0FFFFFFF
        x |= (x >> 8) & 0x00FFFFFF
        x |= (x >> 16)& 0x0000FFFF
        return x + 1

    def b2IsPowerOfTwo(x):
        result = x > 0 and (x & (x - 1)) == 0
        return result
