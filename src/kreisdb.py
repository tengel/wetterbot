#!/usr/bin/python
#
# kreisdb.py - Jabber bot for weather warnings.
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

from landkreis import *

class KreisDb(object):
    # Dictonary: Kreis-String -> Landkreis-Object
    landkreisListeStr = {}
    # Dictionary: Kreis-ID -> Landkreis-Object
    landkreisListeId = {}

    # Dictionary: id -> List: bland  url
    blandListeId = {}
    # Dictionary: blandStr -> List: id  url
    blandListeStr = {}

    instance = None

    # method for singleton pattern
    def __new__(self):
        if KreisDb.instance is None:
            KreisDb.instance = object.__new__(self)
            self.initKreisDb(self.instance)
        return KreisDb.instance

    def initKreisDb(self):
        # fill blandListe from file
        blandFile = open("../data/bland.txt", "r")
        for line in blandFile:
            if line.startswith('#'):
                continue
            m = re.match("(\d+)\s*?\"(.*)\"\s*?\"(.*)\"\s*?", line)
            if m is not None and len(m.groups()) == 3:
                # print "__" + m.group(1) + "__"  + m.group(2) + "__"   + m.group(3) + "__"
                self.blandListeId[ int(m.group(1))] = [m.group(2).__str__(), m.group(3).__str__()]
                self.blandListeStr[m.group(2).__str__().lower()] = [int(m.group(1)), m.group(3).__str__()]
        blandFile.close()

        # fill landkreisListe from file
        kreisFile = open("../data/kreise.txt", "r")
        for line in kreisFile:
            if line.startswith('#'):
                continue
            m = re.match("(\d+)\s+?\"(.*)\"\s+?(\d+)\s+?\"(.*)\"\.*", line)
            if m is not None and len(m.groups())==4:
                # print "__" + m.group(1) + "__"  + m.group(2) + "__"   + m.group(3) + "__"
                k = Landkreis(
                    int(m.group(1)), # id
                    m.group(2).__str__(), # name
                    self.blandListeId.get(int(m.group(3)))[0], # bundesland name
                    self.blandListeId.get(int(m.group(3)))[1], # bundesland url
                    m.group(4).__str__()) # kreis url-part
                self.landkreisListeStr[m.group(2).__str__().lower()] = k
                self.landkreisListeId[int(m.group(1))] = k

        kreisFile.close()

    # Return the Landkreis object for a given landkreis id
    def searchId(self, id):
        return self.landkreisListeId.get(id)

    # Return the Landkreis object for a given landkreis string
    def searchStr(self, kreisStr):
        return self.landkreisListeStr.get(kreisStr.lower())

    # Return the Bundesland-String for a bland-ID
    def searchLandId(self, id):
        landEntry = self.blandListeId.get(id)
        if landEntr is not None:
            return landEntry[0]
        return None

    # Return the bland-id for a Bundesland name
    def searchLandStr(self, blandStr):
        landEntry = self.blandListeStr.get(blandStr.lower())
        if landEntry is not None:
            return landEntry[0]
        return None


    # Return a String with all landkreise.
    # blandStr is a string with the name of a bundesland
    def kreisListeStr(self, blandStr=None):
        kreislisteS = "\n"
        if blandStr is None:
            # no bundeland specifiend, return list of bundeslander
            blandListe = self.blandListeStr.keys()
            blandListe.sort()
            for land in blandListe:
                kreislisteS += land + "\n"
        elif self.searchLandStr(blandStr) is not None:
            kreisliste = []
            for kreis in self.landkreisListeStr.keys():
                if self.landkreisListeStr[kreis].bland.lower().startswith(blandStr.lower()):
                    kreisliste.append(kreis)
            kreisliste.sort()
            for kreis in kreisliste:
                kreislisteS += self.landkreisListeStr[kreis].__str__() + "\n"
        else:
            kreislisteS = "Das Bundesland '" + blandStr + "' kenne ich nicht :-("
        return kreislisteS







