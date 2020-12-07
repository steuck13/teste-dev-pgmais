from message import Message
import unittest

class MessageTest(unittest.TestCase):
    #entry = 'b7e2af69-ce52-4812-adf1-395c8875ad30;46;90816645;CLARO;19:05:21;justo lacinia eget tincidunt eget'
    entry = 'd81b2696-8b62-4b8b-af82-586ce0875ebc;21;983522711;TIM;16:42:48;sit amet eros suspendisse accumsan tortor quis turpis sed ante'

    def setUp(self):
        unittest.TestCase.setUp(self)
        self.msg = Message.from_string(MessageTest.entry)

    def test_from_string(self):
        string = MessageTest.entry.split(';')

        self.assertRaises(Exception, Message.from_string, '')
        self.assertEqual(self.msg.msg_id, string[0])
        self.assertEqual(self.msg.ddd, int(string[1]))
        self.assertEqual(self.msg.number, int(string[2]))
        self.assertEqual(self.msg.cpny, string[3])
        self.assertEqual(self.msg.schedule, string[4])
        self.assertEqual(self.msg.content, ''.join(string[5:]))

    def test_isvalid_ddd(self):
        self.assertTrue(self.msg._isvalid_ddd())

    def test_isvalid_number(self):
        self.assertTrue(self.msg._isvalid_number())

    def test_isfromsp(self):
        self.assertFalse(self.msg._isfrom_sp())

    def test_isvalid_schedule(self):
        self.assertTrue(self.msg._isvalid_schedule())

    def test_isvalid_size(self):
        self.assertTrue(self.msg._isvalid_size())

    def test_ison_blacklist(self):
        self.assertTrue(self.msg._ison_blacklist())

    def validate_message(self):
        self.assertTrue(self.msg.validate_message())

    def test_broker(self):
        self.assertAlmostEqual(self.msg.broker(), 1)
