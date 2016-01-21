import struct
import os
from functools import partial

import utilities
import model
from parser import outputFileType
from enum import Enum


class inputFileType(Enum):
    """flag enum indicating the detected type of the input file"""
    ascii = 1
    binary = 2


class FileManager:
    """reads stl files, then loads coordinates into a data_model, can also write stl files using the data model"""

    def __init__(self, input_file):
        """initializes local variable with the name of the input file and a flag variable with None

        Arguments:
        :param input_file:(string) path of file to be used as input

        Returns None
        """
        self._input_file = input_file
        self.input_file_type = None

    def check_file_status(self):
        """Checks if file exists then opens it and determines if it has binary or ascii format"""

        if not os.path.exists(self._input_file):
            utilities.error("The File does not exist", 1)
        print("file exists")
        _a_file_stream = open(self._input_file, encoding='UTF-8')
        try:
            token = _a_file_stream.readline()
            if token.find('solid') == 0:
                print("file has ascii format")
                self.input_file_type = inputFileType.ascii
                _a_file_stream.close()
                return
        except UnicodeDecodeError:
            print("input not ascii file")
        _a_file_stream.close()
        _b_file_stream = open(self._input_file, 'rb')
        _b_file_stream.seek(80)
        current_file = os.stat(self._input_file)
        if current_file.st_size == struct.unpack('i', _b_file_stream.read(4))[0] * 50 + 84:
            print("file has binary format")
            self.input_file_type = inputFileType.binary
        _b_file_stream.close()

        if self.input_file_type is None:
            utilities.error('Error: file not ascii or binary', 1)

    def read_file(self, input_file, data_model):
        """reads a STL file in ascii or binary format and stores the data in a data model

        Arguments:
        :param data_model: data model in which the read data will be stored
        :param input_file: complete path of input file

        Returns None
        """

        self.check_file_status()

        if self.input_file_type == inputFileType.ascii:
            with open(input_file, 'r') as _fileStream:
                words_list = self.parse_file_ascii(_fileStream)
            data_model.header = self.read_header_ascii(words_list)
            self.read_triangles_ascii(data_model, words_list)

        elif self.input_file_type == inputFileType.binary:
            with open(input_file, 'rb') as _fileStream:
                data_model.header = self.read_header_bin(_fileStream)
                data_model.nr_of_faces = self.read_nr_of_faces(_fileStream)
                self.read_triangles_bin(_fileStream, data_model)

    def read_triangles_ascii(self, data_model, words_list):
        """searches word_list for normals and vertexes and appends their coordinates
         to the data_model triangle list
         :param words_list: (list) list of strings containing the words in the parsed file
         :param data_model: (object instance) data model containing a list of triangle objects
        """
        coordinates_list = self.extract_coord_for_normals_and_vertices(words_list)
        if (len(coordinates_list) % 12) != 0:
            utilities.error('error when reading triangle coordinates', 1)
        nr_of_triangles_in_model = int(len(coordinates_list)/12)
        for nr_of_triangles in range(nr_of_triangles_in_model):
            triangle = model.Triangle()
            for i in range(nr_of_triangles*12, (nr_of_triangles*12) + 3):
                triangle.normal_coordinates.append(coordinates_list[i])
            for j in range((nr_of_triangles*12) + 3, (nr_of_triangles*12) + 12):
                triangle.vertex_list.append(coordinates_list[j])
            if len(triangle.normal_coordinates) == 3 and len(triangle.vertex_list) == 9:
                data_model.triangles.append(triangle)
            elif len(triangle.normal_coordinates) != 3 or len(triangle.vertex_list) != 9:
                utilities.error('file read error: face does not have enough vertexes', 1)
        data_model.nr_of_faces = nr_of_triangles_in_model

    def extract_coord_for_normals_and_vertices(self, words_list):
        """add doc
        :param words_list:
        """
        coordinates_list = []
        for index in range(len(words_list)):
            if words_list[index] == 'facet' and words_list[index + 1] == 'normal':
                index_offset = [2, 3, 4]
                for i in index_offset:
                    try:
                        float_word = float(words_list[index + i])
                    except ValueError:
                        utilities.error('normals coordinate is could not be converted to float', 1)
                    coordinates_list.append(float_word)
            if words_list[index] == 'vertex':
                index_offset = [1, 2, 3]
                for i in index_offset:
                    try:
                        float_word = float(words_list[index + i])
                    except ValueError:
                        utilities.error('vertex coordinate could not be converted to float', 1)
                    coordinates_list.append(float_word)
        return coordinates_list

    def parse_file_ascii(self, _file_stream):
        """parses file by char and returns a list words

        Arguments:
        :param _file_stream -- file stream associated with file being parsed

        Returns list of strings
        """
        words_list = []
        word = ''

        read_one_byte = partial(_file_stream.read, 1)
        for char in iter(read_one_byte, ''):
            whitespace_delimiters = [' ', '\n', '\t', '']
            if char not in whitespace_delimiters:
                word += char
            elif char in whitespace_delimiters:
                if word != "":
                    words_list.append(word)
                    word = ''
        words_list.append(word)
        return words_list

    def read_bytes_from_file(self, _file_stream, nr_of_bytes_to_read):
        """add doc

        Arguments:
        :param nr_of_bytes_to_read: (int) nr of bytes to be read at one
        :param _file_stream: (file stream) stream that has opened the file to be read from

        Returns
        """
        return _file_stream.read(nr_of_bytes_to_read)

    def read_header_ascii(self, words_list):
        """merges all words before the word facet into a string and returns it

        Argument:
        :param words_list: -- list of strings

        Returns a string
        """
        header = ''
        for index in range(len(words_list)):
            if words_list[index] == 'facet':
                break
            header += (words_list[index] + ' ')
        return header

    def read_nr_of_faces(self, _file_stream):
        """always reads and returns the next 4 bytes after header of the file stream passed as argument

        Arguments:
        :param _file_stream: (object instance) file stream object

        Returns number of faces found as integer
        """
        if _file_stream.tell() != 80:
            _file_stream.seek(80)
        length = struct.unpack('i', _file_stream.read(4))[0]
        return length
        #functia asta se testeaza sau nu

    def read_header_bin(self, _file_stream):
        """always reads and returns the first 80 bytes of the filestream passed as argument

        Arguments:
        :param _file_stream:(file stream) file stream object

        Returns first 80 bytes converted to string and stripped of extra symbols

        """
        if _file_stream.tell() != 0:
            _file_stream.seek(0)
        temp = struct.unpack('80s', _file_stream.read(80))
        header = str(temp[0])
        header = header.strip('b\'\\x00')
        return header

    def read_triangles_bin(self, _file_stream, data_model):
        """reads bytes after header, unpacks them according to STL format and appends the coordinates
        to normals and vertex's. Then appends the triangles to the list of triangles in model
        :param data_model: (class instance)data model containing a list of triangle objects
        :param _file_stream: (object instance) file stream object
        """

        if _file_stream.tell() != 80:
            _file_stream.seek(80)
        nr_faces = struct.unpack('i', _file_stream.read(4))[0]
        for i in range(nr_faces):
            triangle = model.Triangle()
            for n in range(3):
                normal = struct.unpack('f', _file_stream.read(4))[0]
                triangle.normal_coordinates.append(normal)
            for count in range(9):
                triangle.vertex_list.append(struct.unpack('f', _file_stream.read(4))[0])
            triangle.byte_count = struct.unpack('h', _file_stream.read(2))
            data_model.triangles.append(triangle)

    def write_to_file(self, output_file_name, output_file_type, data_model, new_header=''):
        """writes data in model to output file of specified type

        Arguments:
        :param output_file_name:(string) name that will be given to created output files
        :param output_file_type:(enum) flag for type (ascii or binary)
        :param data_model:(class instance)  data model containing a list of triangle objects
        :param new_header:(string)  optional string to be written as header

        Returns None
        """

        if output_file_type == outputFileType._ascii:
            with open(output_file_name,'w') as _fileStream:
                self.write_header_ascii(_fileStream, data_model, new_header)
                self.write_triangles_ascii(_fileStream, data_model)

        elif output_file_type == outputFileType._binary:
            with open(output_file_name,'wb') as _fileStream:
                self.write_header_binary(_fileStream, data_model, new_header)
                _fileStream.write(struct.pack('i', data_model.nr_of_faces))
                self.write_triangles_binary(_fileStream, data_model)

    def write_triangles_binary(self, _file_stream, data_model):
        """writes each triangle from data model with the proper binary format

        Arguments:
        :param data_model:(class instance) container with a list of triangle objects containing coordinates
         for normals and vertexes
        :param _file_stream:(file stream) fileStream object

        Returns None
        """

        for nr in range(int(data_model.nr_of_faces)):
            _file_stream.write(struct.pack('3f', data_model.triangles[nr].normal_coordinates[0],
                                           data_model.triangles[nr].normal_coordinates[1],
                                           data_model.triangles[nr].normal_coordinates[2]))
            for index in range(9):
                _file_stream.write(struct.pack('f', data_model.triangles[nr].vertex_list[index]))
            _file_stream.write(struct.pack('h', data_model.triangles[nr].byte_count))

    def write_triangles_ascii(self, _file_stream, data_model):
        """writes each triangle from data model with the proper stl string format

        Arguments:
        :param data_model:(class instance) container with a list of triangle objects containing
         coordinates for normals and vertexes
        :param _file_stream:(file stream) fileStream object

        Returns None
        """
        for nr in range(int(data_model.nr_of_faces)):
            _file_stream.write('\nfacet normal {0:.6f} {1:.6f} {2:.6f}\n'.format(data_model.triangles[nr].normal_coordinates[0],
                                                                                 data_model.triangles[nr].normal_coordinates[1],
                                                                                 data_model.triangles[nr].normal_coordinates[2]))
            _file_stream.write('vertex {0:.6f} {1:.6f} {2:.6f}\n'.format(data_model.triangles[nr].vertex_list[0],
                                                                         data_model.triangles[nr].vertex_list[1],
                                                                         data_model.triangles[nr].vertex_list[2]))
            _file_stream.write('vertex {0:.6f} {1:.6f} {2:.6f}\n'.format(data_model.triangles[nr].vertex_list[3],
                                                                         data_model.triangles[nr].vertex_list[4],
                                                                         data_model.triangles[nr].vertex_list[5]))
            _file_stream.write('vertex {0:.6f} {1:.6f} {2:.6f}\n'.format(data_model.triangles[nr].vertex_list[6],
                                                                         data_model.triangles[nr].vertex_list[7],
                                                                         data_model.triangles[nr].vertex_list[8]))
            _file_stream.write('endloop\n')
            _file_stream.write(('endfacet'))
        _file_stream.write('\nendsolid\n')

    def write_header_binary(self, _file_stream, data_model, new_header):
        """checks for optional header and writes it to open file, otherwise writes header from data model.
        Input header cannot be longer that 80 bytes, if it is shorter padding bytes are added

        Arguments:
        :param new_header:(file stream) fileStream object
        :param data_model:(class instance) container with a list of triangle objects containing coordinates
         for normals and vertexes
        :param _file_stream:(string) optional parameter: user input string to be used as header

        Returns None
        """
        if new_header == '':
            bytes_header = bytes(data_model.header, 'utf-8')
            if len(bytes_header) > 80:
                utilities.error('error: outputfile header too long', 1)
            lenght = len(bytes_header)
            value = struct.pack('{}s'.format(lenght), bytes_header)
            _file_stream.write(value)
            byte_padding = struct.pack('{}x'.format(80-lenght))
            _file_stream.write(byte_padding)
        else:
            bytes_header = bytes(new_header, 'utf-8')
            if len(bytes_header) > 80:
                utilities.error('error: outputfile header too long', 1)
            lenght = len(bytes_header)
            value = struct.pack('{}s'.format(lenght), bytes_header)
            _file_stream.write(value)
            byte_padding = struct.pack('{}x'.format(80-lenght))
            _file_stream.write(byte_padding)

    def write_header_ascii(self, _file_stream, data_model, new_header):
        """checks for optional header and writes it to open file, otherwise writes header from data model.
        If input header does not contain the word solid at beginning, adds it to string.

        Arguments:
        :param new_header:(file stream) fileStream object
        :param data_model:(class instance) container with a list of triangle objects containing coordinates
         for normals and vertexes
        :param _file_stream:(string) optional parameter: user input string to be used as header

        Returns None
        """
        if new_header == '':
            if 'solid' in data_model.header:
                _file_stream.write(data_model.header)
            else:
                header = '{}{}'.format('solid ', data_model.header)
                _file_stream.write(header)
        else:
            if 'solid' in new_header:
                _file_stream.write(new_header)
            else:
                new_header = '{}{}'.format('solid ', new_header)
                _file_stream.write(new_header)






