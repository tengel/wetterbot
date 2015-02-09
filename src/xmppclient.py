#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
#
# xmppclient.py - Jabber bot for weather warnings.
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

import sys,os,xmpp, re
import time
import threading
import Queue
from msg import *
from userliste import *
import logger

class XmppClient(threading.Thread):
    botDebug = [] # 'always']
    msgIn = Queue.Queue()
    msgOut = Queue.Queue()
    userListe = UserListe()

    # send a message to a jabber-user. The message must be a unicode string
    def sendMessage(self, toJid, message):
        logger.log('XMPPCLIENT: sending message to %s ' % toJid)
        if not self.conn.isConnected():
            self.connect()
        self.conn.send(xmpp.protocol.Message(toJid, message))
        time.sleep(1)

    def handlePresence(self, conn, pres):
        fromJid = pres.getFrom().__str__()[0:pres.getFrom().__str__().find("/")]

        logger.log('XMPPCLIENT: presence: %s from: %s' % (pres.getType(), fromJid))

        if pres.getType() is None:
            # user has become available
            self.userListe.setUserAvailable(fromJid)

        elif pres.getType() == 'unavailable':
            # user is offline
            self.userListe.setUserUnavailable(fromJid)

        elif pres.getType() == 'subscribe':
            # user put the bot into the her roster
            self.conn.send(xmpp.protocol.Presence(pres.getFrom(), "subscribed"))
            self.conn.send(xmpp.protocol.Presence(pres.getFrom(), "subscribe"))

        elif pres.getType() == 'subscribed':
            # user granted us to get presence messages
            pass

        elif pres.getType() == 'unsubscribed':
            # user does not allow us to get presence messages
            self.conn.send(xmpp.protocol.Presence(pres.getFrom(), "unsubscribed"))

        elif pres.getType() == 'unsubscribe':
            # user wants to get no more messages
            pass


    # handles incoming messages. parses the command and sends a reply.
    # valid commands are:
    # help        display help
    #
    def handleMessage(self, conn, mess):
        aboMgr = AboMgr()
        command = mess.getBody()
        if command is None:
            return
        sender = mess.getFrom().__str__()[0:mess.getFrom().__str__().find("/")]
                # command = command.encode("iso-8859-1")

        logger.log('XMPPCLIENT: message from: %s: %s' % (sender, command))

        if re.search("help", command, re.IGNORECASE):
            reply = """
Guten Tag, ich bin der Wetterbot.
Ich melde dir Wetterwarnungen in deinem Landkreis.
Gib mir einen Befehl:
help                     Zeigt diese Nachricht
abo <landkreis>      Aboniert Wetterwarnungen fuer einen Landkreis
unabo <landkreis>    Kuendigt das Abo fuer einen Landkreis
status               Zeigt welche Landkreise du aboniert hast.
liste [bundesland]    Zeigt die Verfuegbaren Landkreise (fuer ein Bundesland) an.

Bitte beachte, dass meine Meldungen evtl. nicht zuverlaessing sind und ich auch mal ausfaellen kann!
Fuer weitere Informationen mailto:timo-e at freenet dot de
"""
        elif re.search("unabo", command, re.IGNORECASE):
            # Abo zuende.
            kreisDb = KreisDb()
            aboMgr = AboMgr()
            m = re.search("unabo\s+(.*)", command, re.IGNORECASE)
            if m is not None:
                reply = "Du hast '" + m.group(1) + "' abbestellt."
                landkreis = kreisDb.searchStr(m.group(1))
                if landkreis is None:
                    reply = "Landkreis '" + m.group(1) + "' gibt es nicht."
                else:
                    aboMgr.unAboniere(sender, landkreis)
                    #TODO: Erfolg, kein Erfolg
                    reply = "Landkreis '" + landkreis.__str__() + "' gekuendigt"
            else:
                reply = "Der Befehl lautet\nunabo <landkreis>"


        elif re.search("abo", command, re.IGNORECASE):
            # Neuen Landkreis Abonnieren.
            kreisDb = KreisDb()
            aboMgr = AboMgr()
            m = re.search("abo\s+(.*)", command, re.IGNORECASE)
            if m is not None:
                reply = "Du hast '" + m.group(1) + "' aboniert."
                landkreis = kreisDb.searchStr(m.group(1))
                if landkreis is not None:
                    aboMgr.aboniere(sender, landkreis)
                else:
                    reply = "Den Kreis '" + m.group(1) + "' gib es leider nicht."
            else:
                reply = "Der Befehl lautet\nabo <landkreis>"
        elif re.search("status", command, re.IGNORECASE):
            # Liste der abonnieren Landkreise zeigen
            reply = unicode("Status von ", "iso-8859-1") + sender
            landkreise = aboMgr.checkAbo(sender)
            kreislisteStr = "\n"
            if landkreise is not None and len(landkreise) > 0:
                for landkreis in landkreise:
                    kreislisteStr += landkreis.__str__() + "\n"
                reply = reply + kreislisteStr
            else:
                reply = "Nix aboniert"
            reply = reply + "\n====Aktive Warnungen====\n"
            userListe = UserListe()
            user = userListe.getUser(sender)
            if user is not None:
                for w in user.sent:
                    if not w.isExpired():
                        reply = reply + w.__str__().decode("utf-8")
        elif re.search("liste", command, re.IGNORECASE):
            # Liste aller Bundesländer oder Landkreise anzeigen
            kreisDb = KreisDb()
            m = re.search("liste\s+(.*)", command, re.IGNORECASE)
            if m is not None:
                reply = "Liste aller Landkreise aus '" + m.group(1) + "':"
                reply = reply + kreisDb.kreisListeStr(m.group(1))
            else:
                reply = "Liste der Bundeslaender:"
                reply = reply + kreisDb.kreisListeStr(None)
        else:
            reply = "Hallo, ich bin der Wetterbot.\nMit deinem Befehl konnte ich nichts anfangen.\nVersuch mal 'help'."

        self.sendMessage(mess.getFrom().__str__(), reply)

    def handleDisconnect(self):
        pass
        #self.userListe.initUserListe()


    def __init__(self, config):
        threading.Thread.__init__(self)
        self.config        = config
        self.botResource   = config.get('xmpp', 'resource')
        self.botUsername   = config.get('xmpp', 'username')
        self.botXmppServer = config.get('xmpp', 'xmppserver')
        self.botPassword   = config.get('xmpp', 'password')
        self.shutdownFlag  = 0
        self.connect()

    def connect(self):
        logger.log('XMPPCLIENT: Connecting to %s' % self.botXmppServer)

        retry = 0
        while (retry < 10):
            self.conn=xmpp.Client(self.botXmppServer, debug=self.botDebug)
            conres=self.conn.connect(('jabberd.jabber.ccc.de',80))
            if conres:
                break
            retry += 1
            time.sleep(30)

        if not conres:
            raise Exception('Unable to connect to server %s' % self.botXmppServer)
        if conres<>'tls':
            logger.log('XMPPCLIENT: Warning: unable to estabilish secure connection - TLS failed!')

        authres=self.conn.auth(self.botUsername,self.botPassword, self.botResource)
        if not authres:
            raise Exception('Unable to authorize on %s - check login/password.' % self.botXmppServer)
            sys.exit(1)
        if authres<>'sasl':
            logger.log('XMPPCLIENT: Warning: unable to perform SASL auth os %s. Old authentication method used!' % self.botXmppServer)

        self.conn.RegisterHandler('message', self.handleMessage)
        self.conn.RegisterHandler('presence', self.handlePresence)
        self.conn.RegisterDisconnectHandler(self.handleDisconnect)
        self.conn.sendInitPresence()

    def processMsg(self, msg):
        #print 'mppclient.processMsg ' , msg
        if isinstance(msg, TextMsg):
            self.sendMessage(msg.user, msg.text)
        elif isinstance(msg, WarnMsg):
            sendToList = self.userListe.sendToList(msg.landkreis, msg.warnung)
            for user in sendToList:
                #print "XmppClient.processMsg: " + user.__str__()
                self.sendMessage(user.jid, msg.warnung.__str__())

    def run(self):
        i = 0
        while(not self.shutdownFlag):
            connected = False
            try:
                connected = self.conn.isConnected()
            except:
                connected = false

            if not connected:
                self.connect()  # exception

            self.conn.Process(1)  # exception
            try:
                self.processMsg(self.msgIn.get(False))
            except Queue.Empty:
                pass

            if i > 600:
                self.conn.sendInitPresence()
                i = 0
            i = i+1
        logger.log("XMPPCLIENT: shutdown")


    def shutdown(self):
        self.shutdownFlag = 1


if __name__ == '__main__':
    print "main"
    x = XmppClient()

