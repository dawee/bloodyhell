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



class b2ContactID(object):


    def __init__(self):
        from box2d.collision.features import Features
        self.features = Features()
        self.features._m_id = self
        self._key = 0

    @property
    def key(self):
        return self._key

    def Set(self, id):
        self.set_key(id._key)

    def Copy(self):
        contact_id = b2ContactID()
        contact_id.set_key(self._key)
        return contact_id

    def get_key(self):
        return self._key

    def set_key(self, value):
        self._key = value
        self.features._referenceFace = self._key & 0x000000ff
        self.features._incidentEdge = ((self._key & 0x0000ff00) >> 8) & 0x000000ff
        self.features._incidentVertex = ((self._key & 0x00ff0000) >> 16) & 0x000000ff
        self.features._flip = ((self._key & 0xff000000) >> 24) & 0x000000ff
