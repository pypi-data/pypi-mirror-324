# SPDX-FileCopyrightText: 2024 Julien Rippinger
#
# SPDX-License-Identifier: GPL-3.0-or-later

from compas.geometry import (
    Point as CPoint,
    Line as CLine,
    intersection_line_line_xy,
)
import random
from .config import config


class Projectile:
    """I'm a geometry which is beeing projected around an Axonometry.
    TODO: Implement names and selection by name."""

    def __init__(self):
        self.plane = None  # plane membership is set by parent object
        self.projections = {"xy": [], "yz": [], "zx": [], "xyz": []}


class Point(Projectile):
    """Wrapper for a compas.geometry.Point"""

    from compas.geometry import Point as CPoint

    def __init__(self, **kwargs):
        super().__init__()
        if len(kwargs) == 1:
            # If only one coordinate is provided, raise an error.
            raise ValueError("At least two coordinates must be provided.")
        self.plane = None  # set by parent
        self.x = kwargs.get("x", None)
        self.y = kwargs.get("y", None)
        self.z = kwargs.get("z", None)
        combined_key = ""
        if self.x is not None:
            combined_key += "x"
        if self.y is not None:
            combined_key += "y"
        if self.z is not None:
            combined_key += "z"
        self.key = combined_key
        self.key = "zx" if self.key == "xz" else self.key  # switch order for xz
        # the point which is drawn on the paper
        if self.key == "xy":
            self.data = CPoint(self.x, self.y)
        elif self.key == "yz":
            self.data = CPoint(self.z, self.y)
        elif self.key == "zx":
            self.data = CPoint(self.x, self.z)
        else:
            self.data = CPoint(self.x, self.y, self.z)

    def project(self, distance=None, ref_plane_key=None):
        """Project this Point on another plane"""
        # determine projection origin plane
        if self.plane.key == "xyz":
            assert (
                ref_plane_key
            ), "Provide reference plane key in order to project a point from the XYZ space."
            new_point = None
            if ref_plane_key == "xy":
                # Point was maybe already projected when added to the XYZ axo space
                if self.projections["xy"]:
                    existing_projected_point = self.projections["xy"][
                        0
                    ]  # TODO: use __contains__ ?
                else:
                    new_point = self.plane.reference_planes[ref_plane_key].add_point(
                        Point(x=self.x, y=self.y)
                    )
            elif ref_plane_key == "yz":
                # Point was maybe already projected when added to the XYZ axo space
                if self.projections["yz"]:
                    existing_projected_point = self.projections["yz"][
                        0
                    ]  # TODO: use __contains__ ?
                else:
                    new_point = self.plane.reference_planes[ref_plane_key].add_point(
                        Point(y=self.y, z=self.z)
                    )
            elif ref_plane_key == "zx":
                # Point was maybe already projected when added to the XYZ axo space
                if self.projections["zx"]:
                    existing_projected_point = self.projections["zx"][
                        0
                    ]  # TODO: use __contains__ ?
                else:
                    new_point = self.plane.reference_planes[ref_plane_key].add_point(
                        Point(x=self.x, z=self.z)
                    )

            # Add line to drawing is projection is new
            if new_point:
                self.plane.drawing.add_compas_geometry(
                    [CLine(self.data, new_point.data)]
                )
            else:
                new_point = existing_projected_point  # for the return

            # Project from Axo on Reference Plane
            # TODO: determine projected point
            # projected_point = Point(x=dist, y=dist)
            # self.plane.reference_planes[ref_plane_key].add_point(projected_point)
            # self.projections.append(projected_point)
            # projected_point.projections.append(self)
        else:
            # projection initiated from a reference plane
            assert (
                distance
            ), "Provide (third coordinate value) in order to project the point into XYZ space."
            if self.plane.key == "xy":
                new_point = Point(x=self.x, y=self.y, z=distance)  # data will be update
                ref_plane_key = random.choice(["yz", "zx"])
                if ref_plane_key == "yz":
                    auxilary_point = self.plane.axo.reference_planes[
                        ref_plane_key
                    ].add_point(Point(y=self.y, z=distance))
                elif ref_plane_key == "zx":
                    auxilary_point = self.plane.axo.reference_planes[
                        ref_plane_key
                    ].add_point(Point(x=self.x, z=distance))
            elif self.plane.key == "yz":
                new_point = Point(x=distance, y=self.y, z=self.z)  # data will be update
                ref_plane_key = random.choice(["zx", "xy"])
                if ref_plane_key == "zx":
                    auxilary_point = self.plane.axo.reference_planes[
                        ref_plane_key
                    ].add_point(Point(z=self.z, x=distance))
                elif ref_plane_key == "xy":
                    auxilary_point = self.plane.axo.reference_planes[
                        ref_plane_key
                    ].add_point(Point(y=self.y, x=distance))
            elif self.plane.key == "zx":
                new_point = Point(x=self.x, y=distance, z=self.z)  # data will be update
                ref_plane_key = random.choice(["xy", "yz"])
                if ref_plane_key == "xy":
                    auxilary_point = self.plane.axo.reference_planes[
                        ref_plane_key
                    ].add_point(Point(x=self.x, y=distance))
                elif ref_plane_key == "yz":
                    auxilary_point = self.plane.axo.reference_planes[
                        ref_plane_key
                    ].add_point(Point(z=self.z, y=distance))

            axo_point_data = intersection_line_line_xy(
                CLine.from_point_and_vector(self.data, self.plane.projection_vector),
                CLine.from_point_and_vector(
                    auxilary_point.data,
                    self.plane.axo.reference_planes[ref_plane_key].projection_vector,
                ),
            )

            new_point.data = CPoint(*axo_point_data)
            # draw intersection
            self.plane.drawing.add_compas_geometry(
                [
                    CLine(self.data, axo_point_data),
                    CLine(auxilary_point.data, axo_point_data),
                ]
            )

            self.plane.drawing.add(new_point)
        # TODO: update point projection collection
        return new_point

    def __repr__(self):
        if self.key == "xy":
            repr_str = f"Point(x={self.x}, y={self.y})"
        elif self.key == "yz":
            repr_str = f"Point(y={self.y}, z={self.z})"
        elif self.key == "zx":
            repr_str = f"Point(x={self.x}, z={self.z})"
        else:
            repr_str = f"Point(x={self.x}, y={self.y}, z={self.z})"

        return repr_str

    def __eq__(self, other):
        """Projected points are considered as equal."""
        if not isinstance(other, type(self)):
            # if the other item of comparison is not also of the Point class
            return TypeError(f"Can't compare {self} and {other}")
        elif self.key == other.key:
            return (self.x == other.x) and (self.y == other.y) and (self.z == other.z)
        else:
            common_key = "".join(set(self.key).intersection(other.key))
            if common_key == "xy" or common_key == "yx":
                return (self.x == other.x) and (self.y == other.y)
            elif common_key == "yz" or common_key == "zy":
                return (self.y == other.y) and (self.z == other.z)
            elif common_key == "zx" or common_key == "xz":
                return (self.x == other.x) and (self.z == other.z)
            else:
                return False


class Line:
    def __init__(self):
        pass


class Surface:
    def __init__(self):
        pass


class Plane:
    """Base class for axonometric and reference planes"""

    def __init__(self):
        self.key = None
        self.matrix = None
        self.drawing = None  # Initialize the drawing attribute if needed
        self.objects = []

    def add_point(self, point):
        assert (
            point.key == self.key
        ), f"Point coordinates must follow containing plane coordinates. Plane:{self.key} & Point:{point.key}"
        if self.key == "xyz":
            point.data = self._decompose_axo_point(point)
        else:
            point.data = point.data.transformed(self.matrix)

        self.objects.append(point)
        self.drawing.add(point)
        point.plane = self  # add self as parent
        config.logger.info(f"[NEW OBJECT] Add {point} in {self}")
        config.logger.info(f"[UPDATE] {self}: {self.objects}")
        return point

    def _decompose_axo_point(self, axo_point):
        """
        When a point is added in XYZ space it becomes the intersection of two points.
        Basically adding points in two (random) reference planes and intersecting them
        in the xyz space. That intersection becomes the drawn points' data.
        """

        # make two points
        keys = ["xy", "yz", "zx"]
        k1, k2 = random.sample(keys, 2)

        if k1 == "zx" or k2 == "zx":
            p1 = Point(x=axo_point.x, y=axo_point.y)
            p2 = Point(y=axo_point.y, z=axo_point.z)
            plane1 = self.reference_planes["xy"]
            plane2 = self.reference_planes["yz"]

        if k1 == "yz" or k2 == "yz":
            p1 = Point(x=axo_point.x, y=axo_point.y)
            p2 = Point(z=axo_point.z, x=axo_point.x)
            plane1 = self.reference_planes["xy"]
            plane2 = self.reference_planes["zx"]

        if k1 == "xy" or k2 == "xy":
            p1 = Point(z=axo_point.z, x=axo_point.x)
            p2 = Point(y=axo_point.y, z=axo_point.z)
            plane1 = self.reference_planes["zx"]
            plane2 = self.reference_planes["yz"]

        plane1.add_point(p1)
        plane2.add_point(p2)
        axo_point.projections[p1.plane.key].append(p1)
        axo_point.projections[p2.plane.key].append(p2)

        # add them in respective ReferencePlanes
        axo_point_data = intersection_line_line_xy(
            CLine.from_point_and_vector(p1.data, plane1.projection_vector),
            CLine.from_point_and_vector(p2.data, plane2.projection_vector),
        )
        axo_point_data = CPoint(*axo_point_data)
        # Add points in reference planes to the
        # axo point projections collection

        # draw intersection
        self.drawing.add_compas_geometry(
            [CLine(p1.data, axo_point_data), CLine(p2.data, axo_point_data)]
        )
        return axo_point_data


class ReferencePlane(Plane):
    """
    Represents a reference plane in an axonometric projection.

    Args:
        lines (list): The two lines making up the reference plane axes.
    """

    def __init__(self, line_pair, projection_vector):
        super().__init__()  # Call the parent class constructor if necessary
        self.trihedron: Trihedron | None = None
        self.axes = line_pair
        self.projection_vector = projection_vector
        config.logger.info("RefPlane axes:", self.axes)
        self.matrix_to_coord_plane = None  # TODO

    def __repr__(self):
        return f"Reference Plane {self.key}"
