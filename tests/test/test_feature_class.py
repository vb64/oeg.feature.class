"""
make test T=test_feature_class
"""
from . import TestBase


class TestFeatureClass(TestBase):
    """
    oeg_feature_class
    """
    def test_class_gene(self):
        """
        FeatureClass.GENE
        """
        from oeg_feature_class import FeatureClass, size_class, is_in_limits, MagnetType

        thick = 10
        real = (100, 100, 5)
        calcked = (90, 90, 6)

        self.assertEqual(size_class(real[0], real[1], thick), FeatureClass.GENE)

        self.assertEqual(is_in_limits(calcked, real, thick, magnet_type=MagnetType.MFL), (True, True, True))
        self.assertEqual(is_in_limits(calcked, real, thick, magnet_type=MagnetType.TFI), (True, True, True))
        self.assertEqual(is_in_limits((90, 90, 1), real, 30, magnet_type=MagnetType.TFI), (True, True, False))
        self.assertEqual(is_in_limits((90, 5, 1), real, 30, magnet_type=MagnetType.TFI), (True, False, False))

    def test_class_pitt(self):
        """
        FeatureClass.PITT
        """
        from oeg_feature_class import FeatureClass, size_class, is_in_limits, MagnetType

        thick = 10
        real = (10, 10, 10)
        calcked = (9, 9, 6)

        self.assertEqual(size_class(real[0], real[1], thick), FeatureClass.PITT)

        self.assertEqual(is_in_limits(calcked, real, thick, magnet_type=MagnetType.MFL), (True, True, False))
        self.assertEqual(is_in_limits(calcked, real, thick, magnet_type=MagnetType.TFI), (True, True, False))
        self.assertEqual(is_in_limits((90, 90, 1), real, 30, magnet_type=MagnetType.TFI), (False, False, False))

    def test_class_pinh(self):
        """
        FeatureClass.PINH
        """
        from oeg_feature_class import FeatureClass, size_class, is_in_limits, MagnetType

        thick = 10
        real = (5, 5, 5)
        calcked = (9, 9, 6)

        self.assertEqual(size_class(real[0], real[1], thick), FeatureClass.PINH)

        self.assertEqual(is_in_limits(calcked, real, thick, magnet_type=MagnetType.MFL), (True, True, True))
        self.assertEqual(is_in_limits(calcked, real, thick, magnet_type=MagnetType.TFI), (True, True, True))
        self.assertEqual(is_in_limits((90, 90, 1), real, 30, magnet_type=MagnetType.TFI), (False, False, True))

    def test_class_cisl(self):
        """
        FeatureClass.CISL
        """
        from oeg_feature_class import Error, FeatureClass, size_class, is_in_limits, MagnetType

        thick = 10
        real = (5, 100, 10)
        calcked = (5, 100, 6)

        self.assertEqual(size_class(real[0], real[1], thick), FeatureClass.CISL)
        self.assertEqual(is_in_limits(calcked, real, thick, magnet_type=MagnetType.MFL), (True, True, False))

        with self.assertRaises(Error) as context:
            is_in_limits(calcked, real, thick, magnet_type=MagnetType.TFI)
        self.assertIn("class 'CISL'. Not applicable for method 'TFI'", str(context.exception))

    def test_class_axsl(self):
        """
        FeatureClass.AXSL
        """
        from oeg_feature_class import Error, FeatureClass, size_class, is_in_limits, MagnetType

        thick = 10
        real = (100, 5, 10)
        calcked = (100, 5, 6)

        self.assertEqual(size_class(real[0], real[1], thick), FeatureClass.AXSL)

        self.assertEqual(is_in_limits(calcked, real, thick, magnet_type=MagnetType.TFI), (True, True, False))
        self.assertEqual(is_in_limits((90, 90, 1), real, 30, magnet_type=MagnetType.TFI), (True, False, False))

        with self.assertRaises(Error) as context:
            is_in_limits(calcked, real, thick, magnet_type=MagnetType.MFL)
        self.assertIn("class 'AXSL'. Not applicable for method 'MFL'", str(context.exception))

    def test_class_axgr(self):
        """
        FeatureClass.AXGR
        """
        from oeg_feature_class import FeatureClass, size_class, is_in_limits, MagnetType

        thick = 10
        real = (50, 10, 10)
        calcked = (50, 10, 6)

        self.assertEqual(size_class(real[0], real[1], thick), FeatureClass.AXGR)

        self.assertEqual(is_in_limits(calcked, real, thick, magnet_type=MagnetType.MFL), (True, True, False))
        self.assertEqual(is_in_limits(calcked, real, thick, magnet_type=MagnetType.TFI), (True, True, False))
        self.assertEqual(is_in_limits((90, 90, 1), real, 30, magnet_type=MagnetType.TFI), (False, False, False))

    def test_class_cigr(self):
        """
        FeatureClass.CIGR
        """
        from oeg_feature_class import FeatureClass, size_class, is_in_limits, MagnetType

        thick = 10
        real = (10, 50, 10)
        calcked = (10, 50, 6)

        self.assertEqual(size_class(real[0], real[1], thick), FeatureClass.CIGR)

        self.assertEqual(is_in_limits(calcked, real, thick, magnet_type=MagnetType.MFL), (True, True, False))
        self.assertEqual(is_in_limits(calcked, real, thick, magnet_type=MagnetType.TFI), (True, True, False))

    def test_size_class_wrong(self):
        """
        wrong parameters for FeatureClass calculate
        """
        from oeg_feature_class import Error, size_class

        with self.assertRaises(Error) as context:
            size_class(0, 10, 10)
        self.assertIn('Wrong FeatureClass params', str(context.exception))

        with self.assertRaises(Error) as context:
            size_class(-1, 10, 10)
        self.assertIn('Wrong FeatureClass params', str(context.exception))

    def test_is_in_limits(self):  # pylint: disable=too-many-locals
        """
        compare is_in_limits
        """
        from oeg_feature_class import is_in_limits, size_class, FeatureClass, MagnetType

        thick = 16.6

        length = 90
        width = 12
        depth = 4

        real = (length, width, depth)
        real_class = size_class(length, width, thick)

        self.assertEqual(real_class, FeatureClass.AXSL)

        x_mm = 72
        y_mm = 11
        z_mm = 1
        calcked = (x_mm, y_mm, z_mm)

        length_ok, width_ok, depth_ok = is_in_limits(calcked, real, thick, magnet_type=MagnetType.TFI)

        self.assertEqual(length_ok, True)
        self.assertEqual(width_ok, True)
        self.assertEqual(depth_ok, False)

    def test_small_thick(self):
        """
        wall thick < 10 mm
        """
        from oeg_feature_class import size_class, FeatureClass

        self.assertEqual(size_class(10, 10, 5), FeatureClass.PITT)

    def test_is_detectable(self):
        """
        is_detectable
        """
        from oeg_feature_class import is_detectable, MagnetType

        thick = 10
        self.assertTrue(is_detectable((10, 10, 5), thick, magnet_type=MagnetType.MFL))
        self.assertTrue(is_detectable((10, 10, -1), thick, magnet_type=MagnetType.MFL))
        self.assertFalse(is_detectable((20, 1, -1), thick, magnet_type=MagnetType.MFL))
