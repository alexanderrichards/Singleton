"""Tests for the singleton module."""
import unittest
import mock
from singleton._singleton import singleton, InstantiationError, SingletonMeta


class TestSingletonMeta(unittest.TestCase):
    """Unit tests for SingletonMeta metaclass."""

    def setUp(self):
        @singleton
        class TestClass(object):
            def __init__(self, a, b, c=90):
                self.a, self.b, self.c = a, b, c
        self.test_class = TestClass
        self.assertIsInstance(self.test_class, SingletonMeta)
        self.assertFalse(hasattr(self.test_class, '__instance__'))

    def test_call(self):
        with mock.patch.object(SingletonMeta, "__call__", side_effect=InstantiationError) as p:
            with self.assertRaises(InstantiationError):
                self.test_class(1, 2)
            p.assert_called_with(1, 2)

    def test_get_instance(self):
        return_instance = self.test_class.__new__(self.test_class, 1, 2)
        with mock.patch.object(SingletonMeta, "setup", return_value=return_instance) as p:
            instance = self.test_class.get_instance(1, 2)
            p.assert_called_with(1, 2)
            self.assertIs(instance, return_instance)
            setattr(self.test_class, "__instance__", return_instance)
            other = self.test_class.get_instance()
            p.assert_called_once_with(1, 2)
        self.assertIs(other, instance)
        self.assertIs(other, return_instance)

    def test_setup(self):
        return_instance = self.test_class.__new__(self.test_class, 1, 2)
        with mock.patch.object(self.test_class, "__new__", return_value=return_instance) as p,\
             mock.patch.object(self.test_class, "__init__") as q:
            self.test_class.setup(1, 2)
            p.assert_called_with(self.test_class, 1, 2)
            q.assert_called_with(1, 2)

        self.assertTrue(hasattr(self.test_class, '__instance__'))
        self.assertIsNotNone(self.test_class.__instance__)
        self.assertIsInstance(self.test_class.__instance__, self.test_class)
        self.assertIs(self.test_class.__instance__, return_instance)
        with self.assertRaises(InstantiationError):
            self.test_class.setup(1, 2)


class TestSingletonDecorator(unittest.TestCase):
    """Unit tests for singleton decorator."""

    def test_singleton(self):
        with mock.patch.object(SingletonMeta, "__init__", return_value=None) as p:
            @singleton
            class TestClass(object):
                def __init__(self, a, b, c=90):
                    self.a, self.b, self.c = a, b, c
            namespace = vars(TestClass).copy()
            namespace.pop('__dict__', None)
            namespace.pop('__weakref__', None)
            p.assert_called_once_with(TestClass.__name__, TestClass.__bases__, namespace)


class TestSingleton(unittest.TestCase):
    """Integration tests."""

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
        self.test_class.setup(12, b=98, c=100)
        with self.assertRaises(InstantiationError):
            self.test_class.setup(1, b=2)

    def test_get_instance_then_setup(self):
        """Test a call to setup after a call to get_instance."""
        self.test_class.get_instance(12, b=98, c=100)
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
