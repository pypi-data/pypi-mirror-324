# SPDX-FileCopyrightText: 2024 Julien Rippinger
#
# SPDX-License-Identifier: GPL-3.0-or-later

from .drawing import Drawing
from .geometry import Plane
from .trihedron import Trihedron
from .config import config


class Axonometry(Plane):
    """
    Represents an axonometric projection with given angles.
    Not mouch operations happen on this level, this class is more
    like a collection from which to access Trihedron and ReferencePlane
    objects. But this class also inherits Plane, therefore can be used
    as well to add geometries to the Drawing instance.

    Args:
        *angles (tuple): The architecture angle notation for axonometric projections.

    Notes:
        When adding objects, and they have only two of the x y z, it means they are projecitons in a reference plane.
    """

    def __init__(
        self,
        *angles,
        trihedron_size=100.0,
        trihedron_position=(0, 0),
        ref_planes_distance=100.0,
    ):
        """Here takes place the main setup."""
        super().__init__()  # Call the parent class constructor if necessary
        # self.__angles = tuple(angles)
        config.logger.info(f"[INITIALIZE OBJECT] Axonometry {angles[0]}°/{angles[1]}°")
        self.drawing = Drawing()
        self.key = "xyz"
        self.trihedron = Trihedron(
            tuple(angles),
            position=trihedron_position,
            size=trihedron_size,
            ref_planes_distance=ref_planes_distance,
        )
        self.reference_planes = self.trihedron.reference_planes
        for plane in self.reference_planes.values():
            plane.axo = self  # necessary to evaluate the geometry objects' membership
            plane.drawing = self.drawing  # necessary to draw in plane
            # plane.update_matrix()
        # Add Trihedron to Drawing
        self.drawing.add_compas_geometry(self.trihedron.axes.values())
        for plane in self.reference_planes.values():
            self.drawing.add_compas_geometry(plane.axes)

    def show(self):
        self.drawing.show()

    def save_svg(self, filename, directory="./output/"):
        try:
            with open(directory + filename, "w") as f:
                self.drawing.save_svg(f)
        except FileExistsError:
            config.logger.info("Already exists.")

    def __repr__(self):
        import math

        return f"Axonometry {math.degrees(self.trihedron.axo_angles[0])}°/{math.degrees(self.trihedron.axo_angles[1])}°"

    def __getitem__(self, item):
        if item in self.reference_planes.keys():
            return self.reference_planes[item]
        else:
            return self
