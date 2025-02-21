import unittest

if __name__ == '__main__':
    loader = unittest.TestLoader()
    start_dir = '.'
    suite = loader.discover(start_dir, pattern='Test*.py')
    runner = unittest.TextTestRunner()
    runner.run(suite)
