class DataModel:
    """holds the data for STL models"""

    def __init__(self):
        """add doc"""
        self.header = None
        self.triangles = []
        self.nr_of_faces = 0

class Triangle:
    """each Triangle object holds coordinates for normals and vertexes"""

    def __init__(self):
        """add doc"""
        self.normal_coordinates = []
        self.vertex_list = []
        self.byte_count = 0
