#!/usr/bin/python
#
# abomgr.py - Jabber bot for weather warnings.
#
# Copyright (C) Timo Engel (timo-e@freenet.de), Berlin 2007.
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this library; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
#


import re

from kreisdb import *

class AboMgr(object):
    instance = None

    # method for singleton pattern
    def __new__(self):
        if AboMgr.instance is None:
            AboMgr.instance = object.__new__(self)
            self.initAboMgr(self.instance)
        return AboMgr.instance

    # initialize the AboMgr
    def initAboMgr(self):
        self.abos = {}
        self.kreisDb = KreisDb()
        aboFile = open("../data/abos.txt", "r")
        for line in aboFile:
            if line.startswith('#'):
                continue
            m = re.match("(\S+)\s*(\d+).*", line)
            if m is not None and len(m.groups()) == 2:
                if m.group(1).__str__() in self.abos:
                    self.abos[m.group(1).__str__()].append(
                        self.kreisDb.searchId(int(m.group(2))))
                else:
                    self.abos[m.group(1).__str__()] = [ self.kreisDb.searchId( int(m.group(2)) ) ]
        aboFile.close()
        #print "#####################"
        #print self.abos
        #print "######################"

    # write self.abos to file
    def writeToFile(self):
        aboFile = open("../data/abos.txt", "w")
        for jid in self.abos:
            for landkreis in self.abos[jid]:
                aboFile.write(jid + "\t" + landkreis.id.__str__() + "\n")
        aboFile.close()

    # new subscriber for a specified kreis
    def aboniere(self, jid, landkreis):
        # TODO UserListe updaten
        #print "AboMgr.aboniere( " + jid + ", " + landkreis.__str__() + ") " + landkreis.id.__str__()
        if jid in self.abos:
            self.abos[jid].append(landkreis)
        else:
            self.abos[jid] = [landkreis]
        self.writeToFile()

    # user has unsubscribed one or all landkreise
    def unAboniere(self, jid, landkreis=None):
        if landkreis is not None:
            if self.abos.get(jid).count(landkreis) > 0:
                self.abos.get(jid).remove(landkreis)
        else:
            self.abos.pop(jid)
        self.writeToFile()

    # return a list of subscribed landkreise or None.
    def checkAbo(self, jid):
        #print "AboMgr.checkAbo(" + jid + "): " + self.abos.get(jid).__str__()
        return self.abos.get(jid)

    # return a list of all landkreise which have been subscribed.
    def allKreise(self):
        alleKreise = {}
        for user in self.abos:
            for kreis in self.abos[user]:
                alleKreise[kreis] = 1
        return alleKreise.keys()



