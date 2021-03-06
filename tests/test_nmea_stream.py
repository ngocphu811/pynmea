import os
from unittest import TestCase

from pynmea.streamer import NMEAStream, TMQStream
from pynmea.nmea import RMC, MQA

class TestTMQStream(TestCase):
    """
    Tests for TMQ Streamer, this streamer is peculiar due to the nature of TMQ
    equipment in regard to the NMEA standard. For more details read the comments
    in the implementation.

    What is important to know is that TMQ parsing rules are completely different
    than those of NMEAStream class objects.
    """
    def test__read(self):
        # WARNING!: If data is supplied through file like object, the data MUST be in binary format
        # for TMQ style streamer to work correctly
        test_file = os.path.join(os.path.dirname(__file__), 'test_data',
            'test_data_small.tmq')
        expected_result = [
        '$PTMQA,\x01\x02$M\x08\x05\x91\x02$M\x00*E8',
        '$PTMQA,\x01\x02*M\x08\x05\\\x02*M\x00*76',
        ]
        with open(test_file, 'r') as test_file_fd:
            streamer = TMQStream(stream_obj=test_file_fd)
            next_data = streamer._read()
            data = []
            while next_data:
                data += next_data
                next_data = streamer._read()
                pass

        self.assertEqual(data, expected_result)

    def test__read_data(self):
        expected_result = [
            '$PTMQA,\x01\x02$M\x08\x05\x91\x02$M\x00*E8',
            '$PTMQA,\x01\x02*M\x08\x05\\\x02*M\x00*76',
            ]

        # WARNING!: For TMQStreamer the data MUST be in binary format for streamer to work correctly
        input_data = """$GPRMC,184332.07,A,1929.459,S,02410.381,E,74.00,16.78,210410,0.0,E*46
$PTMQA,\x01\x02$M\x08\x05\x91\x02$M\x00*E8\r\n$GPGGA,184333.07,1929.439,S,02410.387,E,1,04,2.8,100.00,M,-33.9,M,,0000*65
$GPRMC,184444.08,A,1928.041,S,02410.809,E,74.00,16.78,210410,0.0,E*48
$GPGGA,184445.08,1928.021,S,02410.814,E,1,04,2.7,100.00,M,-33.9,M,,0000*6E
$GPGLL,1928.001,S,02410.820,E,184446.08,A,A*79
$GPVTG,16.78,T,,M,74.00,N,137.05,K,A*36
$PTMQA,\x01\x02*M\x08\x05\\\x02*M\x00*76\r\n$GPRMC,184448.08,A,1927.962,S,02410.832,E,74.00,16.78,210410,0.0,E*4B
$GPGGA,184449.08,1927.942,S,02410.838,E,1,04,1.7,100.00,M,-33.9,M,,0000*6C
$GPGLL,1927.922,S,02410.844,E,184450.08,A,A*7B
$GPVTG,16.78,T,,M,74.00,N,137.05,K,A*36"""

        streamer = TMQStream()
        data = streamer._read(data=input_data)

        self.assertEqual(data, expected_result)

    def test__get_type(self):
        streamer = TMQStream()
        sentence = '$GPRMC,184332.07,A,1929.459,S,02410.381,E,74.00,16.78,210410,0.0,E*46'
        self.assertRaises( TypeError, streamer._get_type, sentence)

        sentence = '$PTMQA,\x01\x02$M\x08\x05\x91\x02$M\x00*E8\r\n'
        sen_type = streamer._get_type(sentence)
        self.assertTrue(isinstance(sen_type(), MQA))

    def test_read_data_obj(self):
        test_file = os.path.join(os.path.dirname(__file__), 'test_data',
            'test_data_small.tmq')

        with open(test_file, 'r') as test_file_fd:
            streamer = TMQStream(stream_obj=test_file_fd)
            nmea_objects = streamer.get_objects()

        expected_object_types = ['MQA', 'MQA']

        self.assertEqual(expected_object_types[0], nmea_objects[0].sen_type)
        self.assertEqual(expected_object_types[1], nmea_objects[1].sen_type)

    def test_read_data_obj_raw(self):
        data = """$GPRMC,184332.07,A,1929.459,S,02410.381,E,74.00,16.78,210410,0.0,E*46
$PTMQA,\x01\x02$M\x08\x05\x91\x02$M\x00*E8\r\n$GPGGA,184333.07,1929.439,S,02410.387,E,1,04,2.8,100.00,M,-33.9,M,,0000*65
$GPRMC,184444.08,A,1928.041,S,02410.809,E,74.00,16.78,210410,0.0,E*48
$GPGGA,184445.08,1928.021,S,02410.814,E,1,04,2.7,100.00,M,-33.9,M,,0000*6E
$GPGLL,1928.001,S,02410.820,E,184446.08,A,A*79
$GPVTG,16.78,T,,M,74.00,N,137.05,K,A*36
$PTMQA,\x01\x02*M\x08\x05\\\x02*M\x00*76\r\n$GPRMC,184448.08,A,1927.962,S,02410.832,E,74.00,16.78,210410,0.0,E*4B
$GPGGA,184449.08,1927.942,S,02410.838,E,1,04,1.7,100.00,M,-33.9,M,,0000*6C
$GPGLL,1927.922,S,02410.844,E,184450.08,A,A*7B
$GPVTG,16.78,T,,M,74.00,N,137.05,K,A*36"""

        streamer = TMQStream()
        nmea_objects = streamer.get_objects(data=data)

        expected_object_types = ['MQA', 'MQA']

        self.assertEqual(expected_object_types[0], nmea_objects[0].sen_type)
        self.assertEqual(expected_object_types[1], nmea_objects[1].sen_type)

    def test_read_data_str_raw(self):
        data = """$GPRMC,184332.07,A,1929.459,S,02410.381,E,74.00,16.78,210410,0.0,E*46
$PTMQA,\x01\x02$M\x08\x05\x91\x02$M\x00*E8\r\n$GPGGA,184333.07,1929.439,S,02410.387,E,1,04,2.8,100.00,M,-33.9,M,,0000*65
$GPRMC,184444.08,A,1928.041,S,02410.809,E,74.00,16.78,210410,0.0,E*48
$GPGGA,184445.08,1928.021,S,02410.814,E,1,04,2.7,100.00,M,-33.9,M,,0000*6E
$GPGLL,1928.001,S,02410.820,E,184446.08,A,A*79
$GPVTG,16.78,T,,M,74.00,N,137.05,K,A*36
$PTMQA,\x01\x02*M\x08\x05\\\x02*M\x00*76\r\n$GPRMC,184448.08,A,1927.962,S,02410.832,E,74.00,16.78,210410,0.0,E*4B
$GPGGA,184449.08,1927.942,S,02410.838,E,1,04,1.7,100.00,M,-33.9,M,,0000*6C
$GPGLL,1927.922,S,02410.844,E,184450.08,A,A*7B
$GPVTG,16.78,T,,M,74.00,N,137.05,K,A*36"""

        streamer = TMQStream()
        nmea_objects = streamer.get_strings(data=data)

        expected_result = [
            '$PTMQA,\x01\x02$M\x08\x05\x91\x02$M\x00*E8',
            '$PTMQA,\x01\x02*M\x08\x05\\\x02*M\x00*76',
            ]

        self.assertEqual(expected_result, nmea_objects)


class TestStream(TestCase):
    def test_splits_data_1(self):
        test_data = '$foo,bar,baz*77\n$Meep,wibble,123,321\n'
        streamer = NMEAStream()
        result = streamer._split(test_data)
        self.assertEqual(result, ['foo,bar,baz*77', 'Meep,wibble,123,321'])

    def test_splits_data_2(self):
        test_data = '$foo,bar,baz*77\r$Meep,wibble,123,321\r'
        streamer = NMEAStream()
        result = streamer._split(test_data)
        self.assertEqual(result, ['foo,bar,baz*77', 'Meep,wibble,123,321'])

    def test_splits_data_3(self):
        test_data = '$foo,bar,baz*77\r\n$Meep,wibble,123,321'
        streamer = NMEAStream()
        result = streamer._split(test_data)
        self.assertEqual(result, ['foo,bar,baz*77', 'Meep,wibble,123,321'])

    def test_splits_data_4(self):
        test_data = '$foo,bar,baz*77NOTHING$Meep,wibble,123,321NOTHING'
        streamer = NMEAStream()
        result = streamer._split(test_data, separator='NOTHING')
        self.assertEqual(result, ['foo,bar,baz*77', 'Meep,wibble,123,321'])

    def test__read(self):
        test_file = os.path.join(os.path.dirname(__file__), 'test_data',
                                 'test_data_small.gps')
        expected_result = ['GPRMC,184332.07,A,1929.459,S,02410.381,E,74.00,16.78,210410,0.0,E*46',
                           'GPGGA,184333.07,1929.439,S,02410.387,E,1,04,2.8,100.00,M,-33.9,M,,0000*65',
                           'GPRMC,184444.08,A,1928.041,S,02410.809,E,74.00,16.78,210410,0.0,E*48',
                           'GPGGA,184445.08,1928.021,S,02410.814,E,1,04,2.7,100.00,M,-33.9,M,,0000*6E',
                              'GPGLL,1928.001,S,02410.820,E,184446.08,A,A*79',
                           'GPVTG,16.78,T,,M,74.00,N,137.05,K,A*36',
                           'GPRMC,184448.08,A,1927.962,S,02410.832,E,74.00,16.78,210410,0.0,E*4B',
                           'GPGGA,184449.08,1927.942,S,02410.838,E,1,04,1.7,100.00,M,-33.9,M,,0000*6C',
                           'GPGLL,1927.922,S,02410.844,E,184450.08,A,A*7B',
                           'GPVTG,16.78,T,,M,74.00,N,137.05,K,A*36']
        with open(test_file, 'r') as test_file_fd:
            streamer = NMEAStream(stream_obj=test_file_fd)
            next_data = streamer._read()
            data = []
            while next_data:
                data += next_data
                next_data = streamer._read()
                pass

        self.assertEqual(data, expected_result)

    def test__read_data(self):
        expected_result = ['GPRMC,184332.07,A,1929.459,S,02410.381,E,74.00,16.78,210410,0.0,E*46',
                           'GPGGA,184333.07,1929.439,S,02410.387,E,1,04,2.8,100.00,M,-33.9,M,,0000*65',
                           'GPRMC,184444.08,A,1928.041,S,02410.809,E,74.00,16.78,210410,0.0,E*48',
                           'GPGGA,184445.08,1928.021,S,02410.814,E,1,04,2.7,100.00,M,-33.9,M,,0000*6E',
                           'GPGLL,1928.001,S,02410.820,E,184446.08,A,A*79',
                           'GPVTG,16.78,T,,M,74.00,N,137.05,K,A*36',
                           'GPRMC,184448.08,A,1927.962,S,02410.832,E,74.00,16.78,210410,0.0,E*4B',
                           'GPGGA,184449.08,1927.942,S,02410.838,E,1,04,1.7,100.00,M,-33.9,M,,0000*6C',
                           'GPGLL,1927.922,S,02410.844,E,184450.08,A,A*7B',
                           'GPVTG,16.78,T,,M,74.00,N,137.05,K,A*36']

        input_data = """$GPRMC,184332.07,A,1929.459,S,02410.381,E,74.00,16.78,210410,0.0,E*46
$GPGGA,184333.07,1929.439,S,02410.387,E,1,04,2.8,100.00,M,-33.9,M,,0000*65
$GPRMC,184444.08,A,1928.041,S,02410.809,E,74.00,16.78,210410,0.0,E*48
$GPGGA,184445.08,1928.021,S,02410.814,E,1,04,2.7,100.00,M,-33.9,M,,0000*6E
$GPGLL,1928.001,S,02410.820,E,184446.08,A,A*79
$GPVTG,16.78,T,,M,74.00,N,137.05,K,A*36
$GPRMC,184448.08,A,1927.962,S,02410.832,E,74.00,16.78,210410,0.0,E*4B
$GPGGA,184449.08,1927.942,S,02410.838,E,1,04,1.7,100.00,M,-33.9,M,,0000*6C
$GPGLL,1927.922,S,02410.844,E,184450.08,A,A*7B
$GPVTG,16.78,T,,M,74.00,N,137.05,K,A*36
"""

        streamer = NMEAStream()
        data = streamer._read(data=input_data)
        data += streamer._read(data='')

        self.assertEqual(data, expected_result)

    def test__get_type(self):
        streamer = NMEAStream()
        sentence = '$GPRMC,184332.07,A,1929.459,S,02410.381,E,74.00,16.78,210410,0.0,E*46'
        sen_type = streamer._get_type(sentence)
        self.assertTrue(isinstance(sen_type(), RMC))

    def test_read_data_obj(self):
        test_file = os.path.join(os.path.dirname(__file__), 'test_data',
                                 'test_data_small.gps')

        with open(test_file, 'r') as test_file_fd:
            streamer = NMEAStream(stream_obj=test_file_fd)
            next_data = streamer.get_objects()
            nmea_objects = []
            while next_data:
                nmea_objects += next_data
                next_data = streamer.get_objects()

        expected_object_types = ['RMC', 'GGA', 'RMC', 'GGA', 'GLL',
                                 'VTG', 'RMC', 'GGA', 'GLL', 'VTG']

        self.assertEqual(expected_object_types[0], nmea_objects[0].sen_type)
        self.assertEqual(expected_object_types[1], nmea_objects[1].sen_type)
        self.assertEqual(expected_object_types[2], nmea_objects[2].sen_type)
        self.assertEqual(expected_object_types[3], nmea_objects[3].sen_type)
        self.assertEqual(expected_object_types[4], nmea_objects[4].sen_type)
        self.assertEqual(expected_object_types[5], nmea_objects[5].sen_type)
        self.assertEqual(expected_object_types[6], nmea_objects[6].sen_type)
        self.assertEqual(expected_object_types[7], nmea_objects[7].sen_type)
        self.assertEqual(expected_object_types[8], nmea_objects[8].sen_type)
        self.assertEqual(expected_object_types[9], nmea_objects[9].sen_type)

    def test_read_data_obj_raw(self):
        data = """$GPRMC,184332.07,A,1929.459,S,02410.381,E,74.00,16.78,210410,0.0,E*46
$GPGGA,184333.07,1929.439,S,02410.387,E,1,04,2.8,100.00,M,-33.9,M,,0000*65
$GPRMC,184444.08,A,1928.041,S,02410.809,E,74.00,16.78,210410,0.0,E*48
$GPGGA,184445.08,1928.021,S,02410.814,E,1,04,2.7,100.00,M,-33.9,M,,0000*6E
$GPGLL,1928.001,S,02410.820,E,184446.08,A,A*79
$GPVTG,16.78,T,,M,74.00,N,137.05,K,A*36
$GPRMC,184448.08,A,1927.962,S,02410.832,E,74.00,16.78,210410,0.0,E*4B
$GPGGA,184449.08,1927.942,S,02410.838,E,1,04,1.7,100.00,M,-33.9,M,,0000*6C
$GPGLL,1927.922,S,02410.844,E,184450.08,A,A*7B
$GPVTG,16.78,T,,M,74.00,N,137.05,K,A*36
"""
        streamer = NMEAStream()
        nmea_objects = streamer.get_objects(data=data)
        nmea_objects += streamer.get_objects(data='')

        expected_object_types = ['RMC', 'GGA', 'RMC', 'GGA', 'GLL',
                                 'VTG', 'RMC', 'GGA', 'GLL', 'VTG']

        self.assertEqual(expected_object_types[0], nmea_objects[0].sen_type)
        self.assertEqual(expected_object_types[1], nmea_objects[1].sen_type)
        self.assertEqual(expected_object_types[2], nmea_objects[2].sen_type)
        self.assertEqual(expected_object_types[3], nmea_objects[3].sen_type)
        self.assertEqual(expected_object_types[4], nmea_objects[4].sen_type)
        self.assertEqual(expected_object_types[5], nmea_objects[5].sen_type)
        self.assertEqual(expected_object_types[6], nmea_objects[6].sen_type)
        self.assertEqual(expected_object_types[7], nmea_objects[7].sen_type)
        self.assertEqual(expected_object_types[8], nmea_objects[8].sen_type)
        self.assertEqual(expected_object_types[9], nmea_objects[9].sen_type)

    def test_read_data_str_raw(self):
        data = """$GPRMC,184332.07,A,1929.459,S,02410.381,E,74.00,16.78,210410,0.0,E*46
$GPGGA,184333.07,1929.439,S,02410.387,E,1,04,2.8,100.00,M,-33.9,M,,0000*65
$GPRMC,184444.08,A,1928.041,S,02410.809,E,74.00,16.78,210410,0.0,E*48
$GPGGA,184445.08,1928.021,S,02410.814,E,1,04,2.7,100.00,M,-33.9,M,,0000*6E
$GPGLL,1928.001,S,02410.820,E,184446.08,A,A*79
$GPVTG,16.78,T,,M,74.00,N,137.05,K,A*36
$GPRMC,184448.08,A,1927.962,S,02410.832,E,74.00,16.78,210410,0.0,E*4B
$GPGGA,184449.08,1927.942,S,02410.838,E,1,04,1.7,100.00,M,-33.9,M,,0000*6C
$GPGLL,1927.922,S,02410.844,E,184450.08,A,A*7B
$GPVTG,16.78,T,,M,74.00,N,137.05,K,A*36
"""
        streamer = NMEAStream()
        nmea_objects = streamer.get_strings(data=data)
        nmea_objects += streamer.get_strings(data='')

        expected_result = ['GPRMC,184332.07,A,1929.459,S,02410.381,E,74.00,16.78,210410,0.0,E*46',
                           'GPGGA,184333.07,1929.439,S,02410.387,E,1,04,2.8,100.00,M,-33.9,M,,0000*65',
                           'GPRMC,184444.08,A,1928.041,S,02410.809,E,74.00,16.78,210410,0.0,E*48',
                           'GPGGA,184445.08,1928.021,S,02410.814,E,1,04,2.7,100.00,M,-33.9,M,,0000*6E',
                           'GPGLL,1928.001,S,02410.820,E,184446.08,A,A*79',
                           'GPVTG,16.78,T,,M,74.00,N,137.05,K,A*36',
                           'GPRMC,184448.08,A,1927.962,S,02410.832,E,74.00,16.78,210410,0.0,E*4B',
                           'GPGGA,184449.08,1927.942,S,02410.838,E,1,04,1.7,100.00,M,-33.9,M,,0000*6C',
                           'GPGLL,1927.922,S,02410.844,E,184450.08,A,A*7B',
                           'GPVTG,16.78,T,,M,74.00,N,137.05,K,A*36']

        self.assertEqual(expected_result, nmea_objects)