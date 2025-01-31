# SPDX-FileCopyrightText: 2024 Julien Rippinger
#
# SPDX-License-Identifier: GPL-3.0-or-later

import unittest
from unittest.mock import patch
from axonometry import Axonometry, Point, config


class TestAxonometryProjections(unittest.TestCase):

    def setUp(self):
        self.alpha, self.beta = config.random_valid_angles()
        self.axo = Axonometry(self.alpha, self.beta)
        self.p0 = self.axo.add_point(Point(x=10, y=10, z=30))
        self.p1 = self.axo["xy"].add_point(Point(x=10, y=10))
        self.p2 = self.axo["yz"].add_point(Point(y=5, z=10))
        self.p3 = self.axo["zx"].add_point(Point(z=5, x=10))
        _ = self.p0.project(ref_plane_key="xy")
        _ = self.p0.project(ref_plane_key="yz")
        _ = self.p0.project(ref_plane_key="zx")
        _ = self.p1.project(distance=50)
        _ = self.p2.project(distance=25)
        _ = self.p3.project(distance=15)

    @patch("axonometry.Axonometry.save_svg")
    def test_saving_svg(self, mock_save_svg):
        svg_file = f"test_axo_{self.alpha}-{self.beta}.svg"
        """Test saving an Axonometry instance to a SVG file."""
        self.axo.save_svg(svg_file)
        mock_save_svg.assert_called_once_with(svg_file)

    @patch("axonometry.Axonometry.show")
    def test_display_result(self, mock_show):
        self.axo.show()
        mock_show.assert_called_once()


if __name__ == "__main__":
    unittest.main()
