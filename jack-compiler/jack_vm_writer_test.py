import unittest 
from jack_vm_writer import JackVMWriter, Segment, Command

class TestJackVMWriter(unittest.TestCase):
    def test_write_push(self):
        writer = JackVMWriter()
        self.assertEqual(
            writer.write_push(Segment.CONST, 1), [
            "push constant 1"
        ])
        self.assertEqual(
            writer.write_push(Segment.ARG, 1), [
            "push argument 1"
        ])
        self.assertEqual(
            writer.write_push(Segment.LOCAL, 1), [
            "push local 1"
        ])
        self.assertEqual(
            writer.write_push(Segment.STATIC, 1), [
            "push static 1"
        ])
        self.assertEqual(
            writer.write_push(Segment.THIS, 0), [
            "push this 0"
        ])
        self.assertEqual(
            writer.write_push(Segment.THAT, 1), [
            "push that 1"
        ])
        self.assertEqual(
            writer.write_push(Segment.POINTER, 1), [
            "push pointer 1"
        ])
        self.assertEqual(
            writer.write_push(Segment.TEMP, 4), [
            "push temp 4"
        ])

    def test_write_pop(self):
        writer = JackVMWriter()
        self.assertEqual(
            writer.write_pop(Segment.CONST, 1), [
            "pop constant 1"
        ])
        self.assertEqual(
            writer.write_pop(Segment.ARG, 1), [
            "pop argument 1"
        ])
        self.assertEqual(
            writer.write_pop(Segment.LOCAL, 1), [
            "pop local 1"
        ])
        self.assertEqual(
            writer.write_pop(Segment.STATIC, 1), [
            "pop static 1"
        ])
        self.assertEqual(
            writer.write_pop(Segment.THIS, 0), [
            "pop this 0"
        ])
        self.assertEqual(
            writer.write_pop(Segment.THAT, 1), [
            "pop that 1"
        ])
        self.assertEqual(
            writer.write_pop(Segment.POINTER, 1), [
            "pop pointer 1"
        ])
        self.assertEqual(
            writer.write_pop(Segment.TEMP, 4), [
            "pop temp 4"
        ])

    def test_write_arithmetic(self):
        writer = JackVMWriter()
        self.assertEqual(
            writer.write_arithmetic(Command.ADD), [
            "add"
        ])
if __name__ == "__main__":
    unittest.main()
