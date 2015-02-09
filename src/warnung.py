#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
#
# warnung.py - Jabber bot for weather warnings.
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
from datetime import *
import hashlib

class Warnung:
    severityList = ["unbekannte Warnung",
            "Seewetterwarnung",
            "Wetterwarnung",
            "Warnung vor markantem Wetter",
            "Vorwarnung zur Unwetterwarnung",
            "Unwetterwarnung",
            "Warnung vor extremem Unwetter",
                        "Hitzewarnung",
                        "Warnung vor Stark- und Dauerregen",
                        "UV-Warnung"]

    severity = 0
    expires = 0
    text = ""

    def __cmp__(self, other):
        if self.text == other.text and self.expires == other.expires:
            return 0
        elif self.expires > other.expires or self.text > other.text:
            return 1
        else:
            return -1

    def __hash__(self):
                #print self.text
        m = hashlib.md5()
        m.update(self.text)
        m.update(str(self.expires))
        m.update(str(self.severity))
        r = int(0xfffffff & int(m.hexdigest(), 16))
        return r


    def __init__(self, warningHtml):
        #print "======================================================="
        #print warningHtml

        # grep expire date
        m = re.search("bis:.*?(\d+)\.(\d+)\.(\d+).+?(\d+):(\d+) Uhr",
                  warningHtml, re.DOTALL)
        if m is not None:
            # print m.groups()
            self.expires = datetime(int(m.group(3)), int(m.group(2)),
                        int(m.group(1)), int(m.group(4)),
                        int(m.group(5)))
        else:
            self.expires = 0
        warningTxt = re.sub("<.*>", ""  , warningHtml)
        warningTxt = re.sub("\r"  , ""  , warningTxt)
        warningTxt = re.sub("\n\n", "\n", warningTxt)
        warningTxt = re.sub("\n\n", "\n", warningTxt)
        self.text = warningTxt
        #print "------------------------------------------------------"
        #print self.text
        #print "------------------------------------------------------"

        # grep severity

        if re.search("xxxxxx", warningHtml, re.IGNORECASE):
            self.severity = 1 # Seewetterwarnung

        elif re.search("#ffff00", warningHtml, re.IGNORECASE):
            self.severity = 2  # Wetterwarnung

        elif re.search("#fa9600", warningHtml, re.IGNORECASE):
            self.severity = 3 # Warnung vor markantem Wetter

        elif re.search("#ff0000", warningHtml, re.IGNORECASE):
            self.severity = 5 # Unwetterwarnung

        elif re.search("#xxxxxx", warningHtml, re.IGNORECASE):
            self.severity = 6 # Warnung vor extremen Unwetter

        if re.search("#CC99FF", warningHtml, re.IGNORECASE):
            self.severity = 7 # Hitzwarnung

        if re.search("#66B5FF", warningHtml, re.IGNORECASE):
            self.severity = 8 #  Stark- und Dauerregen

        if re.search("#FF00FF", warningHtml, re.IGNORECASE):
            self.severity = 9 #  UV-Warnung


        #print self.severity
        #print "======================================================="

    def __str__(self):
        s = "\n" + (self.severityList[self.severity] + self.text)
        # print s
        return s

    # returns true, if this messages is expired.
    def isExpired(self):
        return self.expires < datetime.now()

