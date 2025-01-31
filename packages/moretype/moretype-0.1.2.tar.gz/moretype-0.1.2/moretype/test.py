import unittest
from moretype import Link

class TestLink(unittest.TestCase):
    def setUp(self):
        self.link = Link(1, 2, 3, 4, 5)

    def test_init_with_args(self):
        self.assertEqual(str(self.link), "1->2->3->4->5->")

    def test_init_with_target(self):
        link = Link(target=(1, 2, 3))
        self.assertEqual(str(link), "1->2->3->")

    def test_init_without_args_or_target(self):
        link = Link()
        self.assertEqual(str(link), "->")

    def test_getitem_with_slice(self):
        new_link = self.link[1:3]
        self.assertEqual(str(new_link), "2->3->")

    def test_getitem_with_index(self):
        self.assertEqual(self.link[2], 3)

    def test_append(self):
        self.link.append(6)
        self.assertEqual(str(self.link), "1->2->3->4->5->6->")

    def test_insert(self):
        self.link.insert(2, 10)
        self.assertEqual(str(self.link), "1->2->10->3->4->5->")

    def test_remove(self):
        self.link.remove(3)
        self.assertEqual(str(self.link), "1->2->4->5->")

    def test_pop(self):
        item = self.link.pop(1)
        self.assertEqual(item, 2)
        self.assertEqual(str(self.link), "1->3->4->5->")

    def test_reverse(self):
        self.link.reverse()
        self.assertEqual(str(self.link), "5->4->3->2->1->")

    def test_show(self):
        import io
        import sys
        captured_output = io.StringIO()
        sys.stdout = captured_output
        self.link.show()
        sys.stdout = sys.__stdout__
        self.assertEqual(captured_output.getvalue(), "1->2->3->4->5->\n")

    def test_get_with_index(self):
        self.assertEqual(self.link.get(index=2), 3)

    def test_get_with_cut_and_sci(self):
        new_link = self.link.get(cut=3, sci=2)
        self.assertEqual(str(new_link), "1->3->")

    def test_get_with_all_params(self):
        new_link = self.link.get(index=1, cut=4, sci=2)
        self.assertEqual(str(new_link), "2->4->")

    def test_get_with_invalid_params(self):
        with self.assertRaises(TypeError):
            self.link.get(index='a', cut=3, sci=2)

    def test_get_with_invalid_slice(self):
        with self.assertRaises(IndexError):
            self.link.get(index=10)


if __name__ == '__main__':
    unittest.main()
