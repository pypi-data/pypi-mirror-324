from unittest import TestSuite, TextTestRunner

from tests.adtools_tests import ADToolsTests
from tests.process_tree_tests import ProcessTreeTests


def suite():
	s = TestSuite()
	s.addTest(ProcessTreeTests('test_conversion_to_process_tree'))
	s.addTest(ProcessTreeTests('test_to_process_tree_and_back'))
	s.addTest(ADToolsTests('test_conversion_to_adtools_term'))
	return s


if __name__ == '__main__':
	runner = TextTestRunner()
	runner.run(suite())
