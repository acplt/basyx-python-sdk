
import unittest

from aas import model


class ExampleReferable(model.Referable):
    def __init__(self):
        super().__init__()


class ExampleIdentifiable(model.Identifiable):
    def __init__(self):
        super().__init__()


class ReferableTest(unittest.TestCase):
    def test_id_short_constraint_aasd_002(self):
        test_object = ExampleReferable()
        test_object.id_short = ""
        self.assertEqual("", test_object.id_short)
        test_object.id_short = "asdASd123_"
        self.assertEqual("asdASd123_", test_object.id_short)
        test_object.id_short = "AAs12_"
        self.assertEqual("AAs12_", test_object.id_short)
        with self.assertRaises(ValueError):
            test_object.id_short = "98sdsfdAS"
        with self.assertRaises(ValueError):
            test_object.id_short = "_sdsfdAS"
        with self.assertRaises(ValueError):
            test_object.id_short = "asdlujSAD8348@S"
        with self.assertRaises(ValueError):
            test_object.id_short = None

    def test_id_short_constraint_aasd_001(self):
        test_object = ExampleIdentifiable()
        test_object.id_short = None
        self.assertEqual(None, test_object.id_short)


class ExampleNamespace(model.Namespace):
    def __init__(self, values=()):
        super().__init__()
        self.set1 = model.NamespaceSet(self, values)
        self.set2 = model.NamespaceSet(self)


class ModelNamespaceTest(unittest.TestCase):
    _namespace_class = ExampleNamespace

    def setUp(self):
        self.prop1 = model.Property("Prop1", "int")
        self.prop2 = model.Property("Prop2", "int")
        self.prop1alt = model.Property("Prop1", "int")
        self.namespace = self._namespace_class()

    def test_NamespaceSet(self) -> None:
        self.namespace.set1.add(self.prop1)
        self.namespace.set1.add(self.prop2)
        self.assertEqual(2, len(self.namespace.set1))
        self.assertIs(self.prop1, self.namespace.set1.get("Prop1"))
        self.assertIn(self.prop1, self.namespace.set1)
        self.assertNotIn(self.prop1alt, self.namespace.set1)
        self.assertIs(self.namespace, self.prop1.parent)

        with self.assertRaises(KeyError):
            self.namespace.set1.add(self.prop1alt)

        with self.assertRaises(KeyError):
            self.namespace.set1.add(self.prop1alt)

        with self.assertRaises(KeyError):
            self.namespace.set2.add(self.prop2)

        self.namespace.set1.remove(self.prop1)
        self.assertEqual(1, len(self.namespace.set1))
        self.assertIsNone(self.prop1.parent)
        self.namespace.set2.add(self.prop1alt)

        self.assertIs(self.prop2, self.namespace.set1.pop())
        self.assertEqual(0, len(self.namespace.set1))

        self.namespace.set2.clear()
        self.assertIsNone(self.prop1alt.parent)
        self.assertEqual(0, len(self.namespace.set2))

        self.namespace.set1.add(self.prop1)
        self.namespace.set1.discard(self.prop1)
        self.assertEqual(0, len(self.namespace.set1))
        self.assertIsNone(self.prop1.parent)
        self.namespace.set1.discard(self.prop1)

    def test_Namespace(self) -> None:
        with self.assertRaises(KeyError):
            namespace_test = ExampleNamespace([self.prop1, self.prop2, self.prop1alt])
        self.assertIsNone(self.prop1.parent)

        namespace = self._namespace_class([self.prop1, self.prop2])
        self.assertIs(self.prop2, namespace.get_referable("Prop2"))
        with self.assertRaises(KeyError):
            namespace.get_referable("Prop3")


class ExampleOrderedNamespace(model.Namespace):
    def __init__(self, values=()):
        super().__init__()
        self.set1 = model.OrderedNamespaceSet(self, values)
        self.set2 = model.OrderedNamespaceSet(self)


class ModelOrderedNamespaceTest(ModelNamespaceTest):
    _namespace_class = ExampleOrderedNamespace  # type: ignore

    def test_OrderedNamespace(self) -> None:
        # Tests from ModelNamespaceTest are inherited, but with ExampleOrderedNamespace instead of ExampleNamespace
        # So, we only need to test order-related things here
        self.namespace.set1.add(self.prop1)
        self.namespace.set1.insert(0, self.prop2)
        with self.assertRaises(KeyError):
            self.namespace.set2.insert(0, self.prop1alt)
        self.assertEqual((self.prop2, self.prop1), tuple(self.namespace.set1))
        self.assertEqual(self.prop1, self.namespace.set1[1])

        with self.assertRaises(KeyError):
            self.namespace.set1[1] = self.prop2
        prop3 = model.Property("Prop3", "int")
        self.namespace.set1[1] = prop3
        self.assertEqual(2, len(self.namespace.set1))
        self.assertIsNone(self.prop1.parent)
        self.assertIs(self.namespace, prop3.parent)
        self.assertEqual((self.prop2, prop3), tuple(self.namespace.set1))

        del self.namespace.set1[0]
        self.assertIsNone(self.prop2.parent)
        self.assertEqual(1, len(self.namespace.set1))