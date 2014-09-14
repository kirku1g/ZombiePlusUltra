import unittest

from zombie.common import pack_host, unpack_host

class TestPackUnpackHost(unittest.TestCase):
    
    def test_pack_unpack_host(self):
        pack_host()