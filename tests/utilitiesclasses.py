import unittest
import sys
from unittest.mock import Mock
sys.path.insert(0, '/home/ovidiu/PycharmProjects/py_sandbox/trunk/basicstl/tests/testutillities')
sys.path.insert(0, '/home/ovidiu/PycharmProjects/py_sandbox/trunk/basicstl/basicstl')
import utilities
import randommodelgenerator
import model


class MergeVerticesGoodValuesTest(unittest.TestCase):
    """Passes a list of proper values and tests the return"""
    def setUp(self):
        self.min_value = 0.1
        self.max_value = 1
        self.nr_of_faces = 2
        self.merge_threshold = 0.001
        self.nr_of_unique_values = 4

    def test_two_duplicates(self):
        """return should be 3 unique vertices"""
        self.r_data_model = randommodelgenerator.gen_r_model(self.nr_of_faces, self.min_value, self.max_value)

        self.r_data_model.triangles[0].vertex_list[0] = 1
        self.r_data_model.triangles[0].vertex_list[1] = 2
        self.r_data_model.triangles[0].vertex_list[2] = 3
        self.r_data_model.triangles[0].vertex_list[3] = 4
        self.r_data_model.triangles[0].vertex_list[4] = 5
        self.r_data_model.triangles[0].vertex_list[5] = 6
        self.r_data_model.triangles[0].vertex_list[6] = 7
        self.r_data_model.triangles[0].vertex_list[7] = 8
        self.r_data_model.triangles[0].vertex_list[8] = 9
        
        self.r_data_model.triangles[1].vertex_list[0] = 1
        self.r_data_model.triangles[1].vertex_list[1] = 2
        self.r_data_model.triangles[1].vertex_list[2] = 3
        self.r_data_model.triangles[1].vertex_list[3] = 4
        self.r_data_model.triangles[1].vertex_list[4] = 5
        self.r_data_model.triangles[1].vertex_list[5] = 6
        self.r_data_model.triangles[1].vertex_list[6] = 7
        self.r_data_model.triangles[1].vertex_list[7] = 8
        self.r_data_model.triangles[1].vertex_list[8] = 9
        
        self.assertEqual(utilities.merge_vertices_for_statistics(self.r_data_model, self.merge_threshold), 3)

    def test_first_vertex_distinct_in_every_triangle(self):
        """return should be 4 unique vertices"""
        self.r_data_model = randommodelgenerator.gen_r_model(self.nr_of_faces, self.min_value, self.max_value)

        self.r_data_model.triangles[0].vertex_list[0] = 1
        self.r_data_model.triangles[0].vertex_list[1] = 2
        self.r_data_model.triangles[0].vertex_list[2] = 3
        self.r_data_model.triangles[0].vertex_list[3] = 0
        self.r_data_model.triangles[0].vertex_list[4] = 0
        self.r_data_model.triangles[0].vertex_list[5] = 0
        self.r_data_model.triangles[0].vertex_list[6] = 0
        self.r_data_model.triangles[0].vertex_list[7] = 0
        self.r_data_model.triangles[0].vertex_list[8] = 0

        self.r_data_model.triangles[1].vertex_list[0] = 10
        self.r_data_model.triangles[1].vertex_list[1] = 20
        self.r_data_model.triangles[1].vertex_list[2] = 30
        self.r_data_model.triangles[1].vertex_list[3] = 0
        self.r_data_model.triangles[1].vertex_list[4] = 0
        self.r_data_model.triangles[1].vertex_list[5] = 0
        self.r_data_model.triangles[1].vertex_list[6] = 0
        self.r_data_model.triangles[1].vertex_list[7] = 0
        self.r_data_model.triangles[1].vertex_list[8] = 0

        self.assertEqual(utilities.merge_vertices_for_statistics(self.r_data_model, self.merge_threshold), 4)

    def test_two_triangles_all_vertex_distinct(self):
        """return should be 6 unique vertices"""
        self.r_data_model = randommodelgenerator.gen_r_model(self.nr_of_faces, self.min_value, self.max_value)

        self.r_data_model.triangles[0].vertex_list[0] = 1
        self.r_data_model.triangles[0].vertex_list[1] = 2
        self.r_data_model.triangles[0].vertex_list[2] = 3
        self.r_data_model.triangles[0].vertex_list[3] = 4
        self.r_data_model.triangles[0].vertex_list[4] = 5
        self.r_data_model.triangles[0].vertex_list[5] = 6
        self.r_data_model.triangles[0].vertex_list[6] = 7
        self.r_data_model.triangles[0].vertex_list[7] = 8
        self.r_data_model.triangles[0].vertex_list[8] = 9

        self.r_data_model.triangles[1].vertex_list[0] = 10
        self.r_data_model.triangles[1].vertex_list[1] = 20
        self.r_data_model.triangles[1].vertex_list[2] = 30
        self.r_data_model.triangles[1].vertex_list[3] = 40
        self.r_data_model.triangles[1].vertex_list[4] = 50
        self.r_data_model.triangles[1].vertex_list[5] = 60
        self.r_data_model.triangles[1].vertex_list[6] = 70
        self.r_data_model.triangles[1].vertex_list[7] = 80
        self.r_data_model.triangles[1].vertex_list[8] = 90

        self.assertEqual(utilities.merge_vertices_for_statistics(self.r_data_model, self.merge_threshold), 6)

    def test_four_triangle_duplicates(self):
        """return should be 3 unique vertices"""
        self.r_data_model = randommodelgenerator.gen_r_model(4, self.min_value, self.max_value)

        self.r_data_model.triangles[0].vertex_list[0] = 1
        self.r_data_model.triangles[0].vertex_list[1] = 2
        self.r_data_model.triangles[0].vertex_list[2] = 3
        self.r_data_model.triangles[0].vertex_list[3] = 4
        self.r_data_model.triangles[0].vertex_list[4] = 5
        self.r_data_model.triangles[0].vertex_list[5] = 6
        self.r_data_model.triangles[0].vertex_list[6] = 7
        self.r_data_model.triangles[0].vertex_list[7] = 8
        self.r_data_model.triangles[0].vertex_list[8] = 9

        self.r_data_model.triangles[1].vertex_list[0] = 1
        self.r_data_model.triangles[1].vertex_list[1] = 2
        self.r_data_model.triangles[1].vertex_list[2] = 3
        self.r_data_model.triangles[1].vertex_list[3] = 4
        self.r_data_model.triangles[1].vertex_list[4] = 5
        self.r_data_model.triangles[1].vertex_list[5] = 6
        self.r_data_model.triangles[1].vertex_list[6] = 7
        self.r_data_model.triangles[1].vertex_list[7] = 8
        self.r_data_model.triangles[1].vertex_list[8] = 9

        self.r_data_model.triangles[2].vertex_list[0] = 1
        self.r_data_model.triangles[2].vertex_list[1] = 2
        self.r_data_model.triangles[2].vertex_list[2] = 3
        self.r_data_model.triangles[2].vertex_list[3] = 4
        self.r_data_model.triangles[2].vertex_list[4] = 5
        self.r_data_model.triangles[2].vertex_list[5] = 6
        self.r_data_model.triangles[2].vertex_list[6] = 7
        self.r_data_model.triangles[2].vertex_list[7] = 8
        self.r_data_model.triangles[2].vertex_list[8] = 9

        self.r_data_model.triangles[3].vertex_list[0] = 1
        self.r_data_model.triangles[3].vertex_list[1] = 2
        self.r_data_model.triangles[3].vertex_list[2] = 3
        self.r_data_model.triangles[3].vertex_list[3] = 4
        self.r_data_model.triangles[3].vertex_list[4] = 5
        self.r_data_model.triangles[3].vertex_list[5] = 6
        self.r_data_model.triangles[3].vertex_list[6] = 7
        self.r_data_model.triangles[3].vertex_list[7] = 8
        self.r_data_model.triangles[3].vertex_list[8] = 9

        self.assertEqual(utilities.merge_vertices_for_statistics(self.r_data_model, self.merge_threshold), 3)

    def test_four_triangles_all_vertex_distinct(self):
        """return should be 12 unique vertices"""
        self.r_data_model = randommodelgenerator.gen_r_model(4, self.min_value, self.max_value)

        self.r_data_model.triangles[0].vertex_list[0] = 1
        self.r_data_model.triangles[0].vertex_list[1] = 2
        self.r_data_model.triangles[0].vertex_list[2] = 3
        self.r_data_model.triangles[0].vertex_list[3] = 4
        self.r_data_model.triangles[0].vertex_list[4] = 5
        self.r_data_model.triangles[0].vertex_list[5] = 6
        self.r_data_model.triangles[0].vertex_list[6] = 7
        self.r_data_model.triangles[0].vertex_list[7] = 8
        self.r_data_model.triangles[0].vertex_list[8] = 9

        self.r_data_model.triangles[1].vertex_list[0] = 10
        self.r_data_model.triangles[1].vertex_list[1] = 20
        self.r_data_model.triangles[1].vertex_list[2] = 30
        self.r_data_model.triangles[1].vertex_list[3] = 40
        self.r_data_model.triangles[1].vertex_list[4] = 50
        self.r_data_model.triangles[1].vertex_list[5] = 60
        self.r_data_model.triangles[1].vertex_list[6] = 70
        self.r_data_model.triangles[1].vertex_list[7] = 80
        self.r_data_model.triangles[1].vertex_list[8] = 90

        self.r_data_model.triangles[2].vertex_list[0] = 100
        self.r_data_model.triangles[2].vertex_list[1] = 200
        self.r_data_model.triangles[2].vertex_list[2] = 300
        self.r_data_model.triangles[2].vertex_list[3] = 400
        self.r_data_model.triangles[2].vertex_list[4] = 500
        self.r_data_model.triangles[2].vertex_list[5] = 600
        self.r_data_model.triangles[2].vertex_list[6] = 700
        self.r_data_model.triangles[2].vertex_list[7] = 800
        self.r_data_model.triangles[2].vertex_list[8] = 900

        self.r_data_model.triangles[3].vertex_list[0] = 1000
        self.r_data_model.triangles[3].vertex_list[1] = 2000
        self.r_data_model.triangles[3].vertex_list[2] = 3000
        self.r_data_model.triangles[3].vertex_list[3] = 4000
        self.r_data_model.triangles[3].vertex_list[4] = 5000
        self.r_data_model.triangles[3].vertex_list[5] = 6000
        self.r_data_model.triangles[3].vertex_list[6] = 7000
        self.r_data_model.triangles[3].vertex_list[7] = 8000
        self.r_data_model.triangles[3].vertex_list[8] = 9000

        self.assertEqual(utilities.merge_vertices_for_statistics(self.r_data_model, self.merge_threshold), 12)


class GetModelHeaderAndStatisticsGoodValues(unittest.TestCase):
    """Passes a mock data model with proper values and tests the return"""

    def setUp(self):
        """setUp for GetModelHeaderAndStatisticsGoodValues"""
        self.mock_model = Mock()
        self.mock_model.mock_add_spec(model.DataModel(), spec_set=True)

    def test_string_header_normal_value(self):
        """returns a string that merges given header and vertex statistics"""
        attributes = {'header': 'solid created in blender', 'nr_of_faces': 5}
        self.mock_model.configure_mock(**attributes)
        output = 'solid created in blender\t5\t15\n'
        self.assertEqual(utilities.get_model_header_and_statistics(self.mock_model), output)

    def test_string_header_empty_value(self):
        """returned string should only contain statistics"""
        attributes = {'header': '', 'nr_of_faces': 5}
        self.mock_model.configure_mock(**attributes)
        output = '\t5\t15\n'
        self.assertEqual(utilities.get_model_header_and_statistics(self.mock_model), output)

    def test_nr_of_faces_null_value(self):
        """returned string should contain 0 nr of faces and vertices"""
        attributes = {'header': 'solid created in blender', 'nr_of_faces': 0}
        self.mock_model.configure_mock(**attributes)
        output = 'solid created in blender\t0\t0\n'
        self.assertEqual(utilities.get_model_header_and_statistics(self.mock_model), output)


class GetModelHeaderAndStatisticsBadValues(unittest.TestCase):
    """Passes a mock data model with bad values or construction and tests the return"""

    def setUp(self):
        """setUp for GetModelHeaderAndStatisticsGoodValues"""
        self.mock_model = Mock()
        self.mock_model.mock_add_spec(model.DataModel(), spec_set=True)

    def test_header_property_missing_with_assert_raise(self):
        """add doc"""
        attributes = {'header': 'solid created in blender', 'nr_of_faces': 0}
        self.mock_model.configure_mock(**attributes)
        self.mock_model.__delattr__('header')
        self.assertRaises(AttributeError, utilities.get_model_header_and_statistics, self.mock_model)
        #clarification of try catch blocks and assertRaise

    def test_catch_attribute_error_and_create_header_attribute_when_model_missing_header_attribute(self):
        """returned string should contain empty header and 5 nr of faces and 15 vertices"""
        attributes = {'header': 'solid created in blender', 'nr_of_faces': 5}
        self.mock_model.configure_mock(**attributes)
        self.mock_model.__delattr__('header')
        output = '\t5\t15\n'
        self.assertEqual(utilities.get_model_header_and_statistics(self.mock_model), output)


class ModelDataCoordinatesGoodValues(unittest.TestCase):
    """Passes a model with proper values and tests the return"""
    def test_one_triangle_normal_values(self):
        """passes a data model with one triangle, returned string must have proper data and format"""
        self.data_model = model.DataModel()
        self.triangle = model.Triangle()
        for i in range(1, 10):
            self.triangle.vertex_list.append(i)
        for i in range(1, 4):
            self.triangle.normal_coordinates.append(i)
        self.data_model.triangles.append(self.triangle)
        output = 'Triangle 0\nnormal coordinates [1, 2, 3]\nvertices coordinates [1, 2, 3, 4, 5, 6, 7, 8, 9]\n'
        self.assertEqual(utilities.get_model_data_coordinates(self.data_model), output)

    def test_two_triangles_identical_values(self):
        """passes a data model with two triangles, returned string must have proper data and format"""
        self.data_model = model.DataModel()

        for j in range(2):
            self.triangle = model.Triangle()
            for i in range(1, 10):
                self.triangle.vertex_list.append(i)
            for i in range(1, 4):
                self.triangle.normal_coordinates.append(i)
            self.data_model.triangles.append(self.triangle)
        output = 'Triangle 0\nnormal coordinates [1, 2, 3]\nvertices coordinates [1, 2, 3, 4, 5, 6, 7, 8, 9]\n' \
                 'Triangle 1\nnormal coordinates [1, 2, 3]\nvertices coordinates [1, 2, 3, 4, 5, 6, 7, 8, 9]\n'
        self.assertEqual(utilities.get_model_data_coordinates(self.data_model), output)

    def test_model_with_empty_triangle_list_values(self):
        """passes a data model with empty_triangle_list, return must be message that triangle list is empty"""
        self.data_model = model.DataModel()
        output = 'triangle list is empty'
        self.assertEqual(utilities.get_model_data_coordinates(self.data_model), output)


class ModelDataCoordinatesBadValues(unittest.TestCase):
    """Passes a model with proper values and tests the return"""
    def test_wrong_type_object_passed_as_argument(self):
        """passes wrong_type_object_passed_as_argument, return error"""
        #TREBUIE CLARFICAT CE SE PRESUPUNE CA TREBUIE TESTAT
        def bad_function():
            pass
        bad_list = []
        map_object = map(bad_function(), bad_list)
        self.assertRaises(TypeError, map_object)

if __name__ == '__main__':
    unittest.main(verbosity=2)
