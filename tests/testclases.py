import unittest
import sys
sys.path.insert(0, '/home/ovidiu/PycharmProjects/py_sandbox/trunk/basicstl/basicstl')
import testcode


class MergeVerticesGoodValuesTest(unittest.TestCase):
    """Passes a list of proper values and tests the return"""

    good_values = [[0.01, 0.02, 0.05, 0.001, 0.002, 0.000002, 0.000003], [30, 200000, 40000, 1231213],
                   [0.000001, 0.00000006, 0.00000000008, 0.000000213132], []]
    value = 0.001

    def test_returns_type_list(self):
        """merge_vertexes should return type is list"""

        for item in range(len(self.good_values)):
            result = testcode.merge_vertexes(self.good_values[item])
            self.assertTrue(isinstance(result, list))

    def test_difference_less_than_value(self):
        """merge_vertexes should give list with difference between values smaller than value"""
        for item in range(len(self.good_values)):
            result = testcode.merge_vertexes(self.good_values[item])
            for index in range(len(result)-1):
                for sec_index in range(index + 1, len(result)):
                    subtraction = result[index] - result[sec_index]
                    if subtraction < 0:
                        subtraction *= -1
                    self.assertGreaterEqual(subtraction, self.value)


class MergeVerticesBadValuesTest(unittest.TestCase):
    """Passes a list of bad values and tests the function"""
    bad_values = [(200, 100), 'bum', 200]
    value = 0.001

    def test_input_must_be_type_list(self):
        """merge_vertexes should accept only list as param 1"""
        for item in range(len(self.bad_values)):
            self.assertRaises(testcode.InputTypeError, testcode.merge_vertexes, self.bad_values[item])


if __name__ == '__main__':
    unittest.main(verbosity=2)
