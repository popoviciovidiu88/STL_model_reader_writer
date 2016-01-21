import random
import sys
sys.path.insert(0, '/home/ovidiu/PycharmProjects/py_sandbox/trunk/basicstl/basicstl')
import model

def gen_r_model(nr_of_faces, minimum_value, maximum_value, nr_of_v_per_face=3):
    """Returns a data model with random values for coordinates in the ranges input by the user"""
    nr_of_vertices = nr_of_v_per_face * 3
    data_model = model.DataModel()

    for index in range(nr_of_faces):
        face = model.Triangle()
        face.vertex_list = generate_ran_vertex_coord_list(nr_of_vertices, minimum_value, maximum_value)
        data_model.triangles.append(face)
    return data_model

def generate_ran_vertex_coord_list(nr_of_vertices, minimum_value, maximum_value):
    """add doc"""
    vertex_coordinates_list = []
    for i in range(nr_of_vertices):
        random_coordinate = random.uniform(minimum_value, maximum_value)
        vertex_coordinates_list.append(random_coordinate)
    return vertex_coordinates_list
