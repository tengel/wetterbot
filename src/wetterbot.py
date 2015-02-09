#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
#
# wetterbot.py - Jabber bot for weather warnings.
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
# Der Bot meldet sich als an einem Jabber-Server an. Benutzer können ihn
# in ihre Kontaktliste aufnehmen und einzelne Landkreise abonieren.
# Der Bot holt die Wetterwarnungen der entsprechenden Landkreise von der
# Website des DWD und verteilt sie an die Benutzer.
#
# Die Daten der Landkreise stammen aus einem Programm von Benjamin Mussler <bm@bmsev.com>.
#
# Start mit $ ./wetterbot.py & disown
#
#
#
#

import re
import sys
import time
import getopt
import httplib
import signal
import os
import ConfigParser


from meldungssammler import *
from landkreis import *
from xmppclient import *
from abomgr import *
from kreisdb import *
import logger


class WetterBot:

    def __init__(self):
        self.config = ConfigParser.ConfigParser()
        self.config.read('../data/config.txt')
        # Dictionary: Landkreis -> List: Warnung
        self.alleWarnungen = {}
        # fetches wether warnings
        self.meldungsSammler = MeldungsSammler()
        # List of available Landkreise
        self.kreisDb = KreisDb()
        self.shutdownFlag = 0

    # Fetches all necessary messages and updates the
    # dictionary for all landkreise.
    # Expired messges are removed from the list.
    def updateMeldungen(self):
        userListe = UserListe()
        fetchListLandkreis = userListe.allKreise()
        self.alleWarnungen = {}
        if fetchListLandkreis is not None and len(fetchListLandkreis) >0:
            for landkreis in fetchListLandkreis:
                # print "Kreis: ", landkreis
                try:
                    kreisWarnings = self.meldungsSammler.fetchMeldung(landkreis)
                    self.alleWarnungen[landkreis] = kreisWarnings
                except Exception, e:
                    self.meldungsSammler = MeldungsSammler()
                    logger.log("WETTERBOT: Exception occured fetching %s: %s" % (landkreis, e))
                    continue

    def processMsg(self, msg):
        pass

    def run(self):
                while not self.shutdownFlag:
                        try:
                                logger.log("WETTERBOT: startup")
                                self.jabclnt = XmppClient(self.config)
                                self.jabclnt.start()
                                userListe = UserListe()

                                while not self.shutdownFlag:

                                        if (not self.jabclnt.isAlive()):
                                                self.jabclnt = XmppClient(self.config)
                                                self.jabclnt.start()
                                        self.updateMeldungen()
                                        if not self.jabclnt.msgOut.empty():
                                                self.processMsg(self.jabclnt.msgOut.get())

                                        for landkreis in self.alleWarnungen.keys():
                                                for warnung in self.alleWarnungen[landkreis]:
                                                        if userListe.isNew(landkreis, warnung):
                                                                self.jabclnt.msgIn.put(WarnMsg(landkreis, warnung) )
                                        time.sleep(5)
                        except Exception, e:
                                logger.log("WETTERBOT: Exception occured: %s" % e)
                                time.sleep(5)
                        finally:
                                self.jabclnt.shutdown()
                                self.jabclnt.join()


    def shutdown(self):
        logger.log("WETTERBOT: shutdown")
        self.shutdownFlag = 1


wetterbot = WetterBot()



def printUsage():
    print """Usage: wetterbot [OPTION]
    -h    --help        show this message
    -V    --version    show version information"""



def handleSignal(signum, frame):
    wetterbot.shutdown()




if __name__ == '__main__':
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hVs", ["help", "version"])
    except getopt.GetoptError:
        print "Invalid option"
        printUsage()
        sys.exit(2)

    signal.signal(signal.SIGHUP, handleSignal)
    signal.signal(signal.SIGINT, handleSignal)

    for o, a in opts:
        if o in ("-V", "--version"):
            print """WetterBot version 0.1
Copyright 2007 Timo Engel (timo-e@freenet.de)
Dies ist freie Software; in den Quellen befinden sich die Lizenzbedingungen.
Es gibt KEINERLEI Garantie; nicht einmal für die TAUGLICHKEIT oder
VERWENDBARKEIT FÜR EINEN BESTIMMTEN ZWECK."""
            sys.exit()
        if o in ("-h", "--help"):
            printUsage()
            sys.exit()

    wetterbot.run()




