"""Tests for the singleton module."""
import unittest
from singleton._singleton import singleton, InstantiationError, SingletonMeta


class TestSingleton(unittest.TestCase):

    def setUp(self):
        """Setup new singleton class."""
        @singleton
        class TestClass(object):
            def __init__(self, a, b, c=90):
                self.a, self.b, self.c = a, b, c
        self.test_class = TestClass

    def test_get_instance_instantiation(self):
        self.assertIsInstance(self.test_class, SingletonMeta)
        self.assertFalse(hasattr(self.test_class, '__instance__'))
        with self.assertRaises(InstantiationError):
            self.test_class(1, 2)
        instance = self.test_class.get_instance(12, b=98, c=100)
        self.assertTrue(hasattr(self.test_class, '__instance__'))
        self.assertIsNotNone(self.test_class.__instance__)
        self.assertIsInstance(self.test_class.__instance__, self.test_class)
        self.assertEqual(instance.a, 12)
        self.assertEqual(instance.b, 98)
        self.assertEqual(instance.c, 100)

    def test_setup_instantiation(self):
        self.assertFalse(hasattr(self.test_class, '__instance__'))
        with self.assertRaises(InstantiationError):
            self.test_class(1, 2)
        instance = self.test_class.setup(12, b=98, c=100)
        self.assertTrue(hasattr(self.test_class, '__instance__'))
        self.assertIsNotNone(self.test_class.__instance__)
        self.assertIsInstance(self.test_class.__instance__, self.test_class)
        self.assertEqual(instance.a, 12)
        self.assertEqual(instance.b, 98)
        self.assertEqual(instance.c, 100)

    def test_setup_second_call(self):
        self.assertFalse(hasattr(self.test_class, '__instance__'))
        instance = self.test_class.setup(12, b=98, c=100)
        with self.assertRaises(InstantiationError):
            self.test_class.setup(1, b=2)

    def test_get_instance_then_setup(self):
        self.assertFalse(hasattr(self.test_class, '__instance__'))
        instance = self.test_class.get_instance(12, b=98, c=100)
        with self.assertRaises(InstantiationError):
            self.test_class.setup(1, b=2)

    def test_single_object(self):
        self.assertFalse(hasattr(self.test_class, '__instance__'))
        instance = self.test_class.setup(12, b=98)
        self.assertEqual(instance.a, 12)
        self.assertEqual(instance.b, 98)
        self.assertEqual(instance.c, 90)

        other = self.test_class.get_instance(1, b=2)
        self.assertIs(other, instance)


if __name__ == '__main__':
    unittest.main()
