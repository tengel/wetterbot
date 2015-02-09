#!/usr/bin/python
#
# meldungssammler.py - Jabber bot for weather warnings.
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


import httplib
import re

from warnung import *
import logger

class MeldungsSammler:

    def __init__(self):
        self.conn = httplib.HTTPConnection("www.wettergefahren.de")


    def fetchMeldung(self, landkreis):
        self.conn.request("GET", landkreis.url())
        r1 = self.conn.getresponse()
        if r1.status == 200:
            b = r1.read()
            return self.parseNachricht(b)

        else:
            raise Exception('SAMMLER: failed to fetch url %s: status:%s reason:%s' % (landkreis.url(), r1.status, r1.reason))


    # Parses the html file and return a list of Warnung
    def parseNachricht(self, nachricht):
        wList = []  # list of all warnings

        # get all warnings from html
        m = re.match(".+<div class=\"app_ws_div_clear\"></div>(.+)<div class=\"app_ws_create_date\">.+", nachricht, re.DOTALL)
        if m is not None:
            allMessages = m.group(1)
        else:
            raise 'unable to parse message'

        #print "-----------------"
        #print allMessages
        #print "-----------------"

        # parse seperate warnings
        m = re.findall("(<div class=\"app_ws_warning_content_text\".*?</div>)", allMessages, re.DOTALL)
        for warnungHtml in m:
            #print warnungHtml
            #print "---------------------------------------------------"
            w = Warnung(warnungHtml)
            #print w
            wList.append(w)
        return wList

