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


class Features(object):

    _referenceFace = 0
    _incidentEdge = 0
    _incidentVertex = 0
    _flip = 0
    _m_id = None

    def set_referenceFace(self, value):
        self._referenceFace = value
        self._m_id._key = (self._m_id._key & 0xffffff00) | (self._referenceFace & 0x000000ff)

    def get_referenceFace(self):
        return self._referenceFace

    def set_incidentEdge(self,value):
        self._incidentEdge = value
        self._m_id._key = (self._m_id._key & 0xffff00ff) | ((self._incidentEdge << 8) & 0x0000ff00)

    def get_incidentEdge(self):
        return self._incidentEdge

    def set_incidentVertex(self,value):
        self._incidentVertex = value
        self._m_id._key = (self._m_id._key & 0xff00ffff) | ((self._incidentVertex << 16) & 0x00ff0000)

    def get_incidentVertex(self):
        return self._incidentVertex

    def set_flip(self,value):
        self._flip = value
        self._m_id._key = (self._m_id._key & 0x00ffffff) | ((self._flip << 24) & 0xff000000)

    def get_flip(self):
        return self._flip

