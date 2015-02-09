#!/usr/bin/python


import sys
sys.path.append("../src/")

import unittest
from abomgr import *

class AboMgrTest(unittest.TestCase):

	def testSingleton(self):
		i1 = AboMgr()
		i2 = AboMgr()
		self.assertEqual(id(i1), id(i2), "Should be a singleton")

	def testAbo(self):
		i = AboMgr()
                kreisDb = KreisDb()
                landkreis = kreisDb.searchStr("Berlin")
                jid = "bla@blabla.de"
		i.aboniere(jid, landkreis)
                self.assertTrue(i.checkAbo(jid))
                self.assertFalse(i.checkAbo("foo"))
                i.unAboniere(jid)
                self.assertFalse(i.checkAbo(jid))


if __name__ == '__main__':
	unittest.main()
