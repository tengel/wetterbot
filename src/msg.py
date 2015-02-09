#!/usr/bin/python
#
# msg.py - Jabber bot for weather warnings.
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


class Msg:
    def __init__(self, user):
        self.user =  user

### messages from xmpp client to bot

class AboMsg(Msg):
    def __init__(self, user, kreisStr):
        self.kreisStr = kreisStr
        self.user = user

class UnaboMsg(Msg):
    def __init__(self, user, kreisStr):
        self.user = user
        self.kreisStr = kreisStr

class StatusMsg(Msg):
    def __init__(self, user):
        self.user = user

class ListMsg(Msg):
    def __init__(self, user, bland=None):
        self.user = user
        self.bland = bland

### messages from bot to xmpp

class WarnMsg(Msg):
    def __init__(self, landkreis, warnung):
        self.warnung = warnung
        self.landkreis = landkreis

class TextMsg(Msg):
    def __init__(self, user, text):
        self.user = user
        self.text = text
