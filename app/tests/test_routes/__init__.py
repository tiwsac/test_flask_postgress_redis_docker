# Run the added test case via following command:
# python3 "/Applications/PyCharm CE.app/Contents/plugins/python-ce/helpers/pycharm/_jb_pytest_runner.py" --path </path/to/project/app/tests>

from unittest import TestCase


class Tests(TestCase):
    def test_true_is_true(self):
        self.assertTrue(True)
