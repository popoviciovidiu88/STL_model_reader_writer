import sys


def error(error_text="Warning: ", exit_code= 0):
    """Uses print to output a message to console
    and calls sys.exit if passed int value that is different that 0

    Arguments:
    :param exit_code:(int) int that is printed as exit code
    :param error_text:(string) string containing message to be printed

    Returns None
    """
    sys.stderr.write('{}\n'.format(error_text))
    if exit_code != 0:
        sys.exit(exit_code)


def print_model_header_console(data_model, no_merge=False):
    """prints data model header, nr of faces and number of points to console
    :param no_merge:(bool) indicates if vertices should be merged for statistics
    :param data_model:(class instance) the data model holding coordinates for vertices

    Returns None
    """
    print(get_model_header_and_statistics(data_model, no_merge))


def get_model_header_and_statistics(data_model, no_merge=False):
    """gets header and vertex statistics from model, joins them in one string and returns is

    Arguments:
    :param no_merge:(bool) indicates if vertices should be merged for statistics
    :param data_model:(class instance) the data model holding coordinates for vertices

    Returns string
    """
    try:
        header = data_model.header
    except AttributeError as err:
        print('AttributeError: Passed model has no header attr: {}'.format(err))
        data_model.header = ''
        header = data_model.header

    faces = data_model.nr_of_faces
    if no_merge is False:
        vertices = merge_vertices_for_statistics(data_model)
    elif no_merge is True:
        vertices = faces * 3
    data_string = '{}\t{}\t{}\n'.format(header, str(faces), str(vertices))
    return data_string


def merge_vertices_for_statistics(data_model, merge_threshold=0.001):
    """compares coordinates of vertices to each other, returns nr of unique vertices under given threshold
    Arguments:
    :param merge_threshold:(float) vertices with coordinate differences under this value will be merged
    :param data_model:(class instance) the data model holding coordinates for vertices

    Returns int
    """
    distinct_vertices = []
    for vertex_coord in range(3):
        coord_for_first_triangle = (data_model.triangles[0].vertex_list[(vertex_coord*3) + 0],
                                    data_model.triangles[0].vertex_list[(vertex_coord*3) + 1],
                                    data_model.triangles[0].vertex_list[(vertex_coord*3) + 2])
        distinct_vertices.append(coord_for_first_triangle)
    for triangle_index in range(1, len(data_model.triangles)):
        x = len(data_model.triangles)
        for point_index in range(3):
            vertex_is_unique = compare_vertices((triangle_index, point_index), distinct_vertices, data_model,
                                                merge_threshold)
            if vertex_is_unique:
                vertex_coord_tuple = (data_model.triangles[triangle_index].vertex_list[(point_index*3)+0],
                                      data_model.triangles[triangle_index].vertex_list[(point_index*3)+1],
                                      data_model.triangles[triangle_index].vertex_list[(point_index*3)+2])
                distinct_vertices.append(vertex_coord_tuple)
    return len(distinct_vertices)


def compare_vertices(vertex1_index, distinct_vertices_list, data_model, merge_threshold):
    """returns true if abs between given points is less that the merge_threshold
    Arguments:
    :param distinct_vertices_list: (list) vertex coordinates
    :param merge_threshold: (float) difference between vertices is compared to this value
    :param data_model: (object) the data model holding coordinates for vertices
    :param vertex1_index: (tuple) First vertex to be compared. First int is index of triangle, second is index of vertex

    Returns bool
    """
    for nr_of_tuples in range(len(distinct_vertices_list)):
        coordinate_index1 = vertex1_index[1] * 3
        nr_of_matches = 0
        for i in range(3):
            subtraction = data_model.triangles[vertex1_index[0]].vertex_list[coordinate_index1] - \
                          distinct_vertices_list[nr_of_tuples][i]
            if abs(subtraction) < merge_threshold:
                nr_of_matches += 1
            coordinate_index1 += 1
        if nr_of_matches == 3:
            return False
    return True


def print_model_data_console(data_model):
    """prints coordinates for normal and vertex for each triangle in model

    Arguments:
    :param data_model: (class instance) holds the coordinates for the points that describe faces

    Returns None
    """
    print(get_model_data_coordinates(data_model))


def get_model_data_coordinates(data_model):
    """returns the normal and vertices coordinates for a data model as a string

    Arguments:
    :param data_model: (class instance) holds the coordinates for the points that describe faces

    Returns a string
    """
    triangles = ''
    for i in range(len(data_model.triangles)):
        triangle_normals_coord = 'normal coordinates {}'.format(data_model.triangles[i].normal_coordinates)
        triangle_vertex_coord = 'vertices coordinates {}'.format(data_model.triangles[i].vertex_list)
        triangle = 'Triangle {}\n{}\n{}\n'.format(i+1, triangle_normals_coord, triangle_vertex_coord)
        triangles = ''.join([triangles, triangle])
    if triangles == '':
        triangles = 'triangle list is empty'
    return triangles
