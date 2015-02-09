#!/usr/bin/python
#
# landkreis.py - Jabber bot for weather warnings.
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


class Landkreis:
    name = ""
    bland = ""
    blandUrl = ""
    kreisUrl = ""

    def __init__(self, id, name, bland, blandUrl, kreisUrl):
        self.id = id
        self.name = name
        self.bland = bland
        self.blandUrl = blandUrl
        self.kreisUrl = kreisUrl

    def __cmp__(self, other):
        if self.id > other.id:
            return 1
        elif self.id < other.id:
            return -1
        else:
            return 0

    def __hash__(self):
        return self.id

    def __str__(self):
        return (self.name + " (" + self.bland + ")" )

    def url(self):
        if len(self.kreisUrl) == 1:
            urlPart = self.kreisUrl + "XX"
        elif len(self.kreisUrl) == 2:
            urlPart = self.kreisUrl + "X"
        else:
            urlPart = self.kreisUrl
        return "http://www.wettergefahren.de/dyn/app/ws/html/reports/" + urlPart + "_warning_de.html"
