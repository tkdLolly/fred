import unittest

from utils import base64_decode, base64_encode, poll, base64_sanitize, bfs


class SanitizeBase64Test(unittest.TestCase):
    def test_sanitize_base64(self):
        self.assertEqual(base64_sanitize("vhBAgH???AAA"), "vhBAgHAAA")
        self.assertEqual(base64_sanitize("vhBAgH###AAA"), "vhBAgHAAA")


class Base64Test(unittest.TestCase):
    def test_base64_decode(self):
        self.assertEqual(base64_decode(reversed("AA")), 0)
        self.assertEqual(base64_decode(reversed("BA")), 1)
        self.assertEqual(base64_decode(reversed("/A")), 63)
        self.assertEqual(base64_decode(reversed("AB")), 64)
        self.assertEqual(base64_decode(reversed("//")), 4095)

        self.assertEqual(base64_decode(reversed("AAA")), 0)
        self.assertEqual(base64_decode(reversed("abc")), 116442)

    def test_base64_encode(self):
        self.assertEqual(base64_encode(0, 2), "AA")
        self.assertEqual(base64_encode(1, 2), "AB")
        self.assertEqual(base64_encode(63, 2), "A/")
        self.assertEqual(base64_encode(64, 2), "BA")
        self.assertEqual(base64_encode(4095, 2), "//")

        self.assertEqual(base64_encode(0, 3), "AAA")
        self.assertEqual(base64_encode(116442, 3), "cba")


class BFSTest(unittest.TestCase):
    def test_div2_div3(self):
        start = 5040
        list_of_actions = [
            (lambda x: x // 2 if not x % 2 else x),
            (lambda x: x // 3 if not x % 3 else x)
        ]
        states = bfs(start, list_of_actions)
        self.assertEqual(sum(states), sum([5040, 2520, 1680, 840, 560, 280, 140, 70, 35, 420, 210, 105, 1260, 630, 315]))
        self.assertEqual(list(filter(lambda x: x % 2 and x % 3, states)), [35])


class PollTest(unittest.TestCase):
    def test_poll(self):
        test_string = "ghE8Je"
        value, test_string = poll(2, test_string)
        self.assertEqual(value, 2144)
        value, test_string = poll(2, test_string)
        self.assertEqual(value, 3844)
        value, test_string = poll(2, test_string)
        self.assertEqual(value, 1929)


if __name__ == '__main__':
    unittest.main()
