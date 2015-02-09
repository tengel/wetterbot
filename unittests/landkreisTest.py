#!/usr/bin/python

import sys
sys.path.append("../src/")

import unittest
import landkreis

class LandkreisTest(unittest.TestCase):

	def testLandkreis(self):
                l1 = landkreis.Landkreis(1, "Harburg", "Niedersachsen", "HN00",
                                        "WL")
                l2 = landkreis.Landkreis(2, "Foo", "Bar", "abc",
                                        "xyz")
		print l1
                print l1.url()
                self.assertTrue(l1 < l2)

if __name__ == '__main__':
	unittest.main()


