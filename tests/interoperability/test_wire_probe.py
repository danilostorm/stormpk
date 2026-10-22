from pathlib import Path
import importlib.util
import struct
import unittest

p=Path(__file__).resolve().parents[2]/'tools/interoperability/wire_probe.py'
spec=importlib.util.spec_from_file_location('stormpk_wire_probe',p)
m=importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

class ProtocolHeaderTest(unittest.TestCase):
    def test_own_login_header(self):
        result=m.inspect_header(struct.pack('<HBBI',488,0,0,0x48480001))
        self.assertEqual(result['status'],'stormpk-header-candidate')
        self.assertTrue(result['stormpk_login_opcode'])
    def test_invalid_frame_length(self):
        result=m.inspect_header(struct.pack('<HBBI',0,0,0,0x48480001))
        self.assertEqual(result['status'],'invalid-stormpk-frame')
    def test_unknown_opcode_never_claims_login(self):
        result=m.inspect_header(struct.pack('<HBBI',48,0,0,0x12345678))
        self.assertFalse(result['stormpk_login_opcode'])
    def test_partial_header(self):
        self.assertEqual(m.inspect_header(b'\x00\x00')['status'],'incomplete')

if __name__=='__main__':unittest.main()
