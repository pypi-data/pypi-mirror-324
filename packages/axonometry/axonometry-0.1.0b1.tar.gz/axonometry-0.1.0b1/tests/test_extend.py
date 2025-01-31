# SPDX-FileCopyrightText: 2024 Julien Rippinger
#
# SPDX-License-Identifier: GPL-3.0-or-later

import unittest
from axonometry import Axonometry, Drawing


class TestAxonometryLayout(unittest.TestCase):

    def setUp(self):
        self.drawing = Drawing(page_format="A1")

    def test_two_axo_drawing(self):
        axo1 = Axonometry(15, 45)
        axo2 = Axonometry(42.5, 7)
        self.drawing.add_axonometry(axo1)
        self.drawing.add_axonometry(axo2)
        # self.drawing.show()


if __name__ == "__main__":
    unittest.main()
