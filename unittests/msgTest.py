#!/usr/bin/python

import sys
sys.path.append("../src/")

import unittest
from msg import *

class MsgTest(unittest.TestCase):

	def testMsg(self):
		a = AboMsg("icke", "irgendwo")
		b = UnaboMsg("der@da", "asdjkfl")
		c = StatusMsg("user@host.tld")
		d = ListMsg("ich")


if __name__ == '__main__':
	unittest.main()

