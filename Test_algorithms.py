import unittest
from  algorithms import compression_templates
class AlgorithmsTest(unittest.TestCase):
    def test_explandOnByteToPixels_OK(self):
        a = compression_templates()
        x= 10
        result = a.expandOneByteToPixels(x)
        self.assertEqual(result,[0,0,0,0,255,0,255,0])
        x = 255
        result = a.expandOneByteToPixels(x)
        self.assertEqual(result,[255,255,255,255,255,255,255,255])


if __name__ == '__main__':
    unittest.main()