# SPDX-FileCopyrightText: 2024 Julien Rippinger
#
# SPDX-License-Identifier: GPL-3.0-or-later

import unittest
from unittest.mock import patch
from axonometry import Axonometry
from axonometry.config import config


class TestAxonometrySaving(unittest.TestCase):

    def setUp(self):
        self.alpha, self.beta = config.random_valid_angles()
        self.axo = Axonometry(self.alpha, self.beta)

    @patch("axonometry.Axonometry.save_svg")
    def test_saving_svg(self, mock_save_svg):
        svg_file = f"test_axo_{self.alpha}-{self.beta}.svg"
        """Test saving an Axonometry instance to a SVG file."""
        self.axo.save_svg(svg_file)
        mock_save_svg.assert_called_once_with(svg_file)


if __name__ == "__main__":
    unittest.main()
