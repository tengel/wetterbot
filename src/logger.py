#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
#
# logger.py - logger for wetterbot.py
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

import datetime

logfile = '../wetterbot.log'

def log(message):
    m = "";
    try:
        now = datetime.datetime.now()
        file = open(logfile, 'aw')
    except:
        return

    try:
        file.write('[%s] %s\n' % (now, message))
    except:
        try:
            file.write('[%s] %s\n' % (now, message.encode("utf-8")))
        except:
            pass

    try:
        close(file)
    except:
        pass
