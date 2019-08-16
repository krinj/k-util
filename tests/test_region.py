# -*- coding: utf-8 -*-

from unittest import TestCase
from k_util import Region


class TestRegion(TestCase):

    def setUp(self):
        self.r = Region(0, 100, 0, 100)

    def test_region_initialize(self):
        """ Simply initialize a region without error. """
        region = Region(0, 1, 2, 3)
        self.assertEqual(Region, type(region))

    def test_region_side_updates(self):
        """ Check that a region's attributes can be updated properly. """
        self.assertEqual(100, self.r.width)
        self.assertEqual(100, self.r.height)

        self.r.right = 200
        self.r.top = -300

        self.assertEqual(200, self.r.width)
        self.assertEqual(400, self.r.height)

    def test_region_position_updates(self):
        """ Check that a region's attributes can be updated properly. """
        self.assertEqual(50, self.r.x)
        self.assertEqual(50, self.r.y)

        self.r.right = 50
        self.r.bottom = 50

        self.assertEqual(25, self.r.x)
        self.assertEqual(25, self.r.y)

        self.r.x = 0
        self.r.y = 100

        self.assertEqual(-25, self.r.left)
        self.assertEqual(25, self.r.right)
        self.assertEqual(75, self.r.top)
        self.assertEqual(125, self.r.bottom)

        self.r.set_xy(100, 0)

        self.assertEqual(75, self.r.left)
        self.assertEqual(125, self.r.right)
        self.assertEqual(-25, self.r.top)
        self.assertEqual(25, self.r.bottom)

    def test_region_size_updates(self):
        """ Check that a region's attributes can be updated properly. """
        self.r.width = 200
        self.r.height = 400

        self.assertEqual(-50, self.r.left)
        self.assertEqual(150, self.r.right)
        self.assertEqual(-150, self.r.top)
        self.assertEqual(250, self.r.bottom)

        self.r.set_size(10, 10)
        self.assertEqual(45, self.r.left)
        self.assertEqual(55, self.r.right)
        self.assertEqual(45, self.r.top)
        self.assertEqual(55, self.r.bottom)

    def test_region_float(self):
        """ Test the creation of a float region. """
        region = Region(0.0, 0.5, 0.0, 1.3, force_int=False)
        region.x = 60.6
        region.height = 2.5
        region.left = region.left - 1.5
        region.right = region.right - 1.5

        self.assertEqual(0.5, region.width)
        self.assertEqual(2.5, region.height)

    def test_region_print(self):
        """ Can print out a region. """
        print(self.r)

    def test_region_area(self):
        """ Get the area of a region. """
        area = self.r.area
        self.assertEqual(10000, area)

    def test_region_distance(self):
        """ Get distance of a region. """
        r1 = Region(0, 10, 0, 10)
        r2 = Region(0, 10, 0, 10)

        self.assertEqual(0, Region.distance(r1, r2))

        r1.x = 1000
        r2.x = 0
        self.assertEqual(1000, Region.distance(r1, r2))

        r2.y = 1000
        self.assertAlmostEqual(1411, Region.distance(r1, r2), 0)

    def test_region_ratio_expansion(self):
        """ A region can properly expand its ratio. """
        region = Region(0, 100, 0, 200)
        region.expand_to_ratio(1.0)

        self.assertEqual(200, region.width)
        self.assertEqual(region.height, region.width)

        region = Region(0, 500, 0, 100)
        region.expand_to_ratio(1.5)

        self.assertEqual(500, region.width)
        self.assertEqual(500 // 1.5, region.height)

    def test_set_illegal_edges(self):
        """ Region should throw an error if an illegal value is used for the edge. """
        with self.assertRaises(Exception):
            Region(100, 0, 0, 100)

        with self.assertRaises(Exception):
            Region(0, 100, 100, 0)

    def test_contains(self):
        """ Check if the region can detect when it contains a point. """
        self.assertEqual(True, self.r.contains(50, 50))
        self.assertEqual(True, self.r.contains(0, 0))
        self.assertEqual(True, self.r.contains(1, 100))
        self.assertEqual(True, self.r.contains(100, 1))
        self.assertEqual(True, self.r.contains(100, 100))
        self.assertEqual(False, self.r.contains(101, 0))
        self.assertEqual(False, self.r.contains(50, 200))
        self.assertEqual(False, self.r.contains(200, 50))

    def test_in_bounds(self):
        target_region = Region(0, 50, 0, 50)
        target_region.set_xy(50, 50)

        self.assertTrue(target_region.is_in_bounds(100, 100))
        self.assertTrue(target_region.is_in_bounds(80, 80))
        self.assertFalse(target_region.is_in_bounds(70, 70))

        target_region.set_xy(100, 100)
        self.assertTrue(target_region.is_in_bounds(200, 200))
        self.assertFalse(target_region.is_in_bounds(100, 100))

    def test_clone(self):
        r2 = self.r.clone()

        # Is a different instance.
        self.assertNotEqual(self.r, r2)

        # The values are the same.
        self.assertEqual(0, r2.left)
        self.assertEqual(100, r2.right)
        self.assertEqual(100, r2.height)

        # Updating the regions are decoupled.
        self.r.set_xy(100, 100)
        self.assertNotEqual(self.r.x, r2.x)

    def test_scale(self):
        """ Test scaling up and down and asymmetrically. """
        self.r.scale(2.0)
        self.assertEqual(200, self.r.width)
        self.assertEqual(200, self.r.height)

        self.r.set_size(100, 200)
        self.r.scale(0.5)
        self.assertEqual(50, self.r.width)
        self.assertEqual(100, self.r.height)

    def test_biggest_edge(self):
        """ Test that we can retrieve biggest edge both for W and H. """
        self.r.set_size(100, 500)
        self.assertEqual(500, self.r.biggest_edge)

        self.r.set_size(8, 4)
        self.assertEqual(8, self.r.biggest_edge)

    def test_fast_distance(self):
        r1 = Region(0, 10, 0, 10)
        r2 = Region(0, 10, 0, 10)

        r1.set_xy(0, 0)
        r2.set_xy(100, 200)

        self.assertEqual(300, Region.fast_distance(r1, r2))

    def test_region_resize(self):
        """ Check that we can resize the region successfully. """
        r = Region(0, 100, 0, 100)
        r.canvas_resize(0.5)
        self.assertEqual(50, r.width)
        self.assertEqual(50, r.height)

        r = Region(500, 1000, 500, 1000)
        r.canvas_resize(0.5)
        self.assertEqual(250, r.left)
        self.assertEqual(500, r.right)

        r = Region(500, 1000, 500, 1000)
        r.canvas_resize(2)
        self.assertEqual(1000, r.left)
        self.assertEqual(2000, r.right)

    def test_region_clamp(self):
        r1 = Region(-100, 200, -20, 120)

        r1.expand_to_ratio()
        r1.scale(2.5)
        r1.clamp(800, 600)

        print(r1.left, r1.right, r1.top, r1.bottom)

        self.assertGreaterEqual(r1.left, 0)
        self.assertGreaterEqual(r1.right, 0)
        self.assertEqual(r1.width, r1.height)


