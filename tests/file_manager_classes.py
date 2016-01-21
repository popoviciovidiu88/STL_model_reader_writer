import unittest
import sys
import io
from unittest.mock import Mock
#sys.path.insert(0, '/home/ovidiu/PycharmProjects/py_sandbox/trunk/basicstl/tests/testutillities')
sys.path.insert(0, '/home/ovidiu/PycharmProjects/py_sandbox/trunk/basicstl/basicstl')
import utilities
#import randommodelgenerator
import fileManager


class ParseFileAsciiGoodValues(unittest.TestCase):
    """passes a io.StringIO object with proper values and tests the return"""

    def setUp(self):
        self.test_stream = io.StringIO()
        self.test_file_manager_object = fileManager.FileManager('bla')

    def test_normal_string_text(self):
        """add doc"""
        self.test_stream.write('This is story stream 0.00001 0.00055')
        self.test_stream.seek(0)
        expected_output = ['This', 'is', 'story', 'stream', '0.00001', '0.00055']
        self.assertEqual(self.test_file_manager_object.parse_file_ascii(self.test_stream), expected_output)

    def test_text_with_unusual_punctuation(self):
        """add doc"""
        self.test_stream.write('This is story , stream 0.00001 0.00055')
        self.test_stream.seek(0)
        expected_output = ['This', 'is', 'story', ',', 'stream', '0.00001', '0.00055']
        self.assertEqual(self.test_file_manager_object.parse_file_ascii(self.test_stream), expected_output)

    def test_empty_text_file(self):
        """add doc"""
        self.test_stream.write('')
        self.test_stream.seek(0)
        expected_output = ['']
        self.assertEqual(self.test_file_manager_object.parse_file_ascii(self.test_stream), expected_output)
    #think of possible bad values


class ReadHeaderAsciiGoodValues(unittest.TestCase):
    """passes a list of strings and checks if method returns proper string"""

    def test_normal_words_in_list(self):
        """add doc"""
        word_list = ['this', 'is', 'test', 'header', 'facet', 'normal']
        expected_output = 'this is test header '
        self.assertEqual(fileManager.FileManager.read_header_ascii(fileManager.FileManager, word_list), expected_output)
        #proper passing of self as filemanager.FileManager?

    def test_no_words_in_list(self):
        """add doc"""
        word_list = []
        expected_output = ''
        self.assertEqual(fileManager.FileManager.read_header_ascii(fileManager.FileManager, word_list), expected_output)

    def test_no_header_ending_keyword_in_list(self):
        """add doc"""
        word_list = ['this', 'is', 'test', 'header', 'normal']
        expected_output = 'this is test header normal '
        self.assertEqual(fileManager.FileManager.read_header_ascii(fileManager.FileManager, word_list), expected_output)


class ExtractCoordForNormalsAndVerticesGoodValues(unittest.TestCase):
    """add doc"""

    def test_one_triangle_proper_STL_format(self):
        """add doc"""
        input_word_list = ['facet', 'normal', '0.000001', '1.000000', '-1.000000', 'outer', 'loop', 'vertex',
                           '1.000000', '1.000000', '-1.000000', 'vertex', '1.000000', '-1.000000', '-1.000000',
                           'vertex', '-1.000000', '-1.000000', '-1.000000', 'endloop', 'endfacet']
        output = ['0.000001', '1.000000', '-1.000000', '1.000000', '1.000000', '-1.000000',
                  '1.000000', '-1.000000', '-1.000000', '-1.000000', '-1.000000', '-1.000000']
        float_output = [float(coord) for coord in output]
        self.test_file_manager_object = fileManager.FileManager('bla')
        self.assertEqual(self.test_file_manager_object.extract_coord_for_normals_and_vertices(input_word_list), float_output)

    def test_three_triangles_proper_STL_format(self):
        """add doc"""
        input_word_list = ['facet', 'normal', '0.000001', '1.000000', '-1.000000', 'outer', 'loop', 'vertex',
                           '1.000000', '1.000000', '-1.000000', 'vertex', '1.000000', '-1.000000', '-1.000000',
                           'vertex', '-1.000000', '-1.000000', '-1.000000', 'endloop', 'endfacet', 'facet', 'normal',
                           '0.000000', '0.000000', '-1.000000', 'outer', 'loop', 'vertex', '-1.000000', '-1.000000',
                           '-1.000000', 'vertex', '-1.000000', '1.000000', '-1.000000', 'vertex', '1.000000',
                           '1.000000', '-1.000000', 'endloop', 'endfacet', 'facet', 'normal', '0.000000', '0.000000',
                           '1.000000', 'outer', 'loop', 'vertex',
                           '1.000000', '0.999999', '1.000000', 'vertex', '-1.000000', '1.000000', '1.000000',
                           'vertex', '-1.000000', '-1.000000', '1.000000', 'endloop', 'endfacet']

        output = ['0.000001', '1.000000', '-1.000000', '1.000000', '1.000000', '-1.000000',
                  '1.000000', '-1.000000', '-1.000000', '-1.000000', '-1.000000', '-1.000000', '0.000000', '0.000000',
                  '-1.000000', '-1.000000', '-1.000000', '-1.000000', '-1.000000', '1.000000', '-1.000000',
                  '1.000000', '1.000000', '-1.000000', '0.000000', '0.000000', '1.000000', '1.000000', '0.999999',
                  '1.000000', '-1.000000', '1.000000', '1.000000', '-1.000000', '-1.000000', '1.000000']
        float_output = [float(coord) for coord in output]
        self.test_file_manager_object = fileManager.FileManager('bla')
        self.assertEqual(self.test_file_manager_object.extract_coord_for_normals_and_vertices(input_word_list), float_output)

    def test_one_triangle_proper_STL_format_preceded_by_header_words(self):
        """add doc"""
        input_word_list = ['solid', 'header', 'is', 'here', 'facet', 'normal', '0.000001', '1.000000', '-1.000000',
                           'outer', 'loop', 'vertex',
                           '1.000000', '1.000000', '-1.000000', 'vertex', '1.000000', '-1.000000', '-1.000000',
                           'vertex', '-1.000000', '-1.000000', '-1.000000', 'endloop',
                           'endfacet', 'solid', 'header', 'is', 'here']
        output = ['0.000001', '1.000000', '-1.000000', '1.000000', '1.000000', '-1.000000',
                  '1.000000', '-1.000000', '-1.000000', '-1.000000', '-1.000000', '-1.000000']
        float_output = [float(coord) for coord in output]
        self.test_file_manager_object = fileManager.FileManager('bla')
        self.assertEqual(self.test_file_manager_object.extract_coord_for_normals_and_vertices(input_word_list), float_output)

if __name__ == '__main__':
    unittest.main(verbosity=2)