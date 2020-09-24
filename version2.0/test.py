import unittest

import main


class MyTestCase(unittest.TestCase):
    def test_something(self):
        self.assertEqual(main.calc_of_similarity("他来到了网易杭研大厦", "小明硕士毕业于中国科学院计算所"), 0)


if __name__ == '__main__':
    unittest.main()
