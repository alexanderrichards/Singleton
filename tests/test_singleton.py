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
        self.assertIsInstance(self.test_class, SingletonMeta)
        self.assertFalse(hasattr(self.test_class, '__instance__'))

    def tearDown(self):
        """Check singleton internals were setup correctly."""
        self.assertTrue(hasattr(self.test_class, '__instance__'))
        self.assertIsNotNone(self.test_class.__instance__)
        self.assertIsInstance(self.test_class.__instance__, self.test_class)

    def test_get_instance_instantiation(self):
        """Test instantiation with get_instance."""
        with self.assertRaises(InstantiationError):
            self.test_class(1, 2)
        with self.assertRaises(TypeError):
            instance = self.test_class.get_instance()
        with self.assertRaises(TypeError):
            instance = self.test_class.get_instance(12)
        instance = self.test_class.get_instance(12, b=98, c=100)
        self.assertEqual(instance.a, 12)
        self.assertEqual(instance.b, 98)
        self.assertEqual(instance.c, 100)

    def test_setup_instantiation(self):
        """Test instantiation with setup."""
        with self.assertRaises(InstantiationError):
            self.test_class(1, 2)
        with self.assertRaises(TypeError):
            instance = self.test_class.setup()
        with self.assertRaises(TypeError):
            instance = self.test_class.setup(12)
        instance = self.test_class.setup(12, b=98, c=100)
        self.assertEqual(instance.a, 12)
        self.assertEqual(instance.b, 98)
        self.assertEqual(instance.c, 100)

    def test_setup_second_call(self):
        """Test a second call to setup."""
        instance = self.test_class.setup(12, b=98, c=100)
        with self.assertRaises(InstantiationError):
            self.test_class.setup(1, b=2)

    def test_get_instance_then_setup(self):
        """Test a call to setup after a call to get_instance."""
        instance = self.test_class.get_instance(12, b=98, c=100)
        with self.assertRaises(InstantiationError):
            self.test_class.setup(1, b=2)

    def test_single_object(self):
        """Test that we do indeed only create one object instance."""
        instance = self.test_class.setup(12, b=98)
        self.assertEqual(instance.a, 12)
        self.assertEqual(instance.b, 98)
        self.assertEqual(instance.c, 90)

        other = self.test_class.get_instance(1, b=2)
        self.assertIs(other, instance)


if __name__ == '__main__':
    unittest.main()
