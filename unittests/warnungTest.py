#!/usr/bin/python

import sys
sys.path.append("../src")
import unittest

from warnung import *

class WarnungTest(unittest.TestCase):
    msg = ""

    def setUp(self):
        msg = """<table width=100% border=0 bordercolor=#F0F805>
          <tr><td bgcolor=#F0F805 width=10>&nbsp;</td><td>

<br>
<br>Amtliche WARNUNG vor STURMB&Ouml;EN
<br>
<br>f&uuml;r Landkreis Wernigerode , Bergland oberhalb 1000 Meter
<br>
<br>g&uuml;ltig von: Donnerstag, 30.08.07 20:00 Uhr
<br>       bis: Freitag, 31.08.07 06:00 Uhr
<br>
<br>ausgegeben vom Deutschen Wetterdienst
<br>        am: Donnerstag, 30.08.07 19:07 Uhr
<br>
<br>Auflebender westlicher Wind, der in B&ouml;en 65 bis 85 km/h
<br>(entspricht 18 bis 24 m/s oder windst&auml;rke 8 bis 9) erreicht.
<br>
<br>Hinweis auf m&ouml;gliche Gefahren:
<br>- einzelne herabst&uuml;rzende &Auml;ste, herabfallende Gegenst&auml;nde
<br>
<br>DWD / RZ Leipzig
<br>=
<br><br></td></table>"""

        w = Warnung(msg)


    def testExpire(self):
        w = Warnung("  bis: Freitag, 30.08.207 06:00 Uhr  ")
        self.assert_(w.isExpired(), "Expire Failed. Should be expired." )

        w = Warnung("  bis: Freitag, 30.08.2020 06:00 Uhr  ")
        self.failIf(w.isExpired(), "Expire Failed. Should not be expired." )



if __name__ == '__main__':
        unittest.main()

