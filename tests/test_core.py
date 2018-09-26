# -*- coding: utf-8 -*-

from unittest import TestCase
from k_util import core


class TestCore(TestCase):

    # ======================================================================================================================
    # Main Test Methods.
    # ======================================================================================================================

    def test_lerp(self):

        # Lerp different float values.

        self.lerp_and_check(v1=0, v2=100, f=0.5, result=50)
        self.lerp_and_check(v1=100, v2=200, f=0.3, result=130)
        self.lerp_and_check(v1=500, v2=0, f=0.8, result=100)
        self.lerp_and_check(v1=1, v2=2, f=0.5, result=1.5)
        self.lerp_and_check(v1=-100, v2=300, f=0.75, result=200)

    def test_lerp_color(self):

        # Test that we can interpolate a variety of colors at different factors.

        self.lerp_color_and_check(
            c1=(0, 0, 0),
            c2=(120, 100, 80),
            f=0.5,
            result=(60, 50, 40)
        )
        self.lerp_color_and_check(
            c1=(0, 0, 0),
            c2=(100, 200, 400),
            f=0.25,
            result=(25, 50, 100)
        )
        self.lerp_color_and_check(
            c1=(0, 0, 0),
            c2=(123, 456, 789),
            f=1.0,
            result=(123, 456, 789)
        )

    def test_filter_value(self):

        filtered_value = core.filter_value(10, 20, 0.5)
        self.assertAlmostEqual(15, filtered_value)

    # ======================================================================================================================
    # Support Methods.
    # ======================================================================================================================

    def lerp_color_and_check(self, c1, c2, f, result):
        output_color = core.interpolate_color(c1, c2, f)
        self.assertSequenceEqual(result, output_color)

    def lerp_and_check(self, v1, v2, f, result):
        output_value = core.interpolate(v1, v2, f)
        self.assertEqual(result, output_value)

