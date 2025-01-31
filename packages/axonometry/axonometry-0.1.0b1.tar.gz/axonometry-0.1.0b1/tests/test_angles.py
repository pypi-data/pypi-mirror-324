# SPDX-FileCopyrightText: 2024 Julien Rippinger
#
# SPDX-License-Identifier: GPL-3.0-or-later

import unittest
from axonometry import Axonometry


class TestAxonometryAngles(unittest.TestCase):

    def test_angles(self):
        """Test creating Axonometry instances with series of angles."""
        for alpha in range(0, 91):
            for beta in range(0, 91):
                if (
                    180 - (alpha + beta) >= 90
                    and not (alpha == 0 and beta == 0)
                    and not (alpha == 90 and beta == 0)
                    and not (alpha == 0 and beta == 90)
                ):
                    """Test with valid angle pair."""
                    ax = Axonometry(alpha, beta)
                    self.assertIsNotNone(ax, f"Failed with alpha={alpha}, beta={beta}")
                else:
                    """Test with invalid angle pair."""
                    with self.assertRaises(
                        AssertionError,
                        msg=f"Accepted invalid angle pair (alpha={alpha}, beta={beta}",
                    ):
                        Axonometry(alpha, beta)


if __name__ == "__main__":
    unittest.main()
