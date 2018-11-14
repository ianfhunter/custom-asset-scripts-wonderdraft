import unittest
import os.path

from file_system import *

class TestSVGConversion(unittest.TestCase):

    def test_saveWrite(self):
        circ = """<svg xmlns="http://www.w3.org/2000/svg" width="500" height="500">
<circle cx="250" cy="250" r="210" fill="#fff" stroke="#000" stroke-width="8"/>
</svg>"""
        saveWrite(circ, "bar.svg")
        saveWrite(circ, "foo/bar.svg")
        self.assertTrue(os.path.isfile("bar.svg"))
        self.assertTrue(os.path.isfile("foo/bar.svg"))

    def test_colorFile(self):
        testA = """
# Color Scheme Name,Variation Letter,Color A,Color B,Color C
Temperate,a,c9c832,a2a552,7f8534
Temperate,b,aec9b3,48a16f,287359
Cold,a,f7f9fb,c2dbdf,71a2a6
Cold,b,8dfdff,48b8ba,07909f
Autumn,a,f48b53,f9c00f,ae1543
"""

        testB = """
# Optionally Define Colors to replace (default are pure R, G & B)
> 639393,d4d2bd,3b7a69,757162

# Color Scheme Name,Variation Letter,Color A ... Color Z
Temperate,a,ff0000,00ff00,ff00ff,00ffff
Temperate,b,aec9b3,48a16f,287359,fc00de
Cold,a,f7f9fb,c2dbdf,71a2a6,fc00de
Cold,b,8dfdff,48b8ba,07909f,fc00de
Autumn,a,f48b53,f9c00f,ae1543,fc00de
"""

        testC = """
# Color Scheme Name,Variation Letter,Color A,Color B,Color C
Temperate ,a,c9c832,a2a552,7f8534,,,,,
        Temperate,b  ,aec9b3,48a16f,287359,,,,    ,, , , ,
Cold,a,   ,,f7f9fb , c2dbdf,71a2a6,,,
Cold,b,8dfdff,48b8ba,07909f    ,
Autumn,,  ,a  ,f48b53,,,,f9c00f,  ae1543
"""


        for x in [testA, testB, testC]:
            fn = "testfile.txt"

            f = open(fn, "w")
            f.write(x)
            f.close()

            a = readColorSchemeFile_Colors(file=fn)
            b = readColorSchemeFile_Themes(file=fn)

            self.assertTrue(len(a) > 0)
            self.assertTrue(len(b) > 0)

class TestPNGConversion(unittest.TestCase):

    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')

if __name__ == '__main__':
    unittest.main()