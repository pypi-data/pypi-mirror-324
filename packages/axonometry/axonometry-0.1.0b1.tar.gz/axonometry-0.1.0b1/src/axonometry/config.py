# SPDX-FileCopyrightText: 2024 Julien Rippinger
#
# SPDX-License-Identifier: GPL-3.0-or-later

import pathlib
import logging
import random

pathlib.Path("output/").mkdir(parents=True, exist_ok=True)


class Config:
    def __init__(self):
        self.css_pixel = 3.7795275591
        self.din = {
            "A1": {
                "portrait": (594 * self.css_pixel, 841 * self.css_pixel),
                "landscape": (841 * self.css_pixel, 594 * self.css_pixel),
            }
        }
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        fh = logging.FileHandler("output/debug.log")
        fh.setLevel(logging.DEBUG)
        formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
        fh.setFormatter(formatter)
        self.logger.addHandler(fh)

    def random_valid_angles(self):
        alpha = random.choice([a for a in range(0, 91)])
        beta = random.choice([b for b in range(0, 91)])
        while not (
            180 - (alpha + beta) >= 90
            and not (alpha == 0 and beta == 0)
            and not (alpha == 90 and beta == 0)
            and not (alpha == 0 and beta == 90)
        ):
            alpha = random.choice([a for a in range(0, 91)])
            beta = random.choice([b for b in range(0, 91)])

        return (alpha, beta)


config = Config()
