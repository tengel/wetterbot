#!/usr/bin/pyton
#
# userliste.py - Jabber bot for weather warnings.
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

from abomgr import *

# manage online users
class UserListe(object):
    instance = None

    # method for singleton pattern
    def __new__(self):
        if UserListe.instance is None:
            UserListe.instance = object.__new__(self)
            self.initUserListe(self.instance)
        return UserListe.instance


    def initUserListe(self):
        self.list = []


    def setUserAvailable(self, jid):
        u = User(jid)
        if self.list.count(u) < 1:
            self.list.append(u)


    def setUserUnavailable(self, jid):
        u = User(jid)
        try:
            self.list.remove(u)
        except ValueError:
            pass


    # Return the users to which the warnung has to be send.
    # Adds the warning to the list of sent warnings.
    def sendToList(self, kreis, warnung):
        retList = []
        for user in self.list:
            if user.hasLandkreis(kreis) and  not user.hasSentAdd(warnung):
                retList.append(user)
        return retList


    # return true, if the warning has to be send
    def isNew(self, kreis, warnung):
        for user in self.list:
            if user.hasLandkreis(kreis) and not user.hasSent(warnung):
                return 1
        return 0

    # return a list of all needed landkreise
    def allKreise(self):
        allKreise = []
        # print "UserListe.allKreise()"
        for user in self.list:
            if user.kreise is not None:
                allKreise.extend( user.kreise )
        return allKreise

    # return a User-object for this jid
    def getUser(self, jid):
        for user in self.list:
            if user.jid.lower() == jid.lower():
                return user
        return None

# An online user
class User:

    def __init__(self, jid):
        aboMgr = AboMgr()
        # string with jabberID
        self.jid = jid
        # Landkreis[] alle abonierten landkreise des benutzers
        self.kreise = aboMgr.checkAbo(jid)
        # {Warnung: 1} Map der gesendeten Nachrichten
        self.sent = {}

    # return true, if the given warning has not been sent.
    # Adds the warning to the list of sent warnings
    def hasSentAdd(self, warnung):
        if self.sent.has_key(warnung):
            return 1
        else:
            self.sent[warnung] = 1
            return 0

    # return true, if given warning has not been sent.
    def hasSent(self, warnung):
        if self.sent.has_key(warnung):
            return 1
        else:
            return 0


    # return true, if the user has subscribed to the given landkreis
    def hasLandkreis(self, sKreis):
        if self.kreise is None:
            return 0
        for kreis in self.kreise:
            #print kreis.__str__() + " <-> " + sKreis.__str__()
            if kreis == sKreis:
                #print "    true"
                return 1
        return 0

    def __str__(self):
        return self.jid + ": " + self.kreise.__str__()

    def __cmp__(self, other):
        if self.jid == other.jid:
            return 0
        elif self.jid < other.jid:
            return -1
        else:
            return 1
