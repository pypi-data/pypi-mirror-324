# SPDX-FileCopyrightText: 2024 Julien Rippinger
#
# SPDX-License-Identifier: GPL-3.0-or-later

from vpype import Document, LineCollection, circle, write_svg
from vpype_cli import execute
from compas.geometry import Line as CLine
from compas.geometry import Point as CPoint
from compas.geometry import Polyline as CPolyline

from .config import config


class Drawing:
    """
    I record all what is happening. I am a wrapper of a vpype.Document adding custom methods
    """

    def __init__(self, page_format="A1", page_layout="portrait"):
        # self.__px = 3.7795275591
        self.dimensions = config.din[page_format][page_layout]
        self.document = Document(page_size=self.dimensions)
        self.traces = []

    def resize_page(self, page_format, page_layout):
        raise NotImplementedError

    def add(self, object, layer_id=None):
        self.traces.append(object)
        compas_data = [object.data]  # it's the compas data which is being drawn
        self._print_geometry(compas_data)
        geometry = self.__convert_compas_to_vpype_lines(compas_data)
        self.document.add(geometry)

    def show(self):
        # move geometry into center of page
        self.document.translate(self.dimensions[0] / 2, self.dimensions[1] / 2)
        execute("show --colorful", document=self.document)

    def save_svg(self, filepath):
        # use vpype to save file
        write_svg(output=filepath, document=self.document, center=True)

    def add_axonometry(self, axo, position=None):
        if position:
            axo.drawing.document.translate()  # TODO compute translate from new position
        self.document.extend(axo.drawing.document)

    def add_compas_geometry(self, compas_data):
        # no traces ?
        self._print_geometry(compas_data)
        geometry = self.__convert_compas_to_vpype_lines(compas_data)
        self.document.add(geometry)

    def __convert_compas_to_shapely(self, compas_geometry):
        """Convert a Compas geometry object to a Shapely LineString."""
        from shapely import LineString

        if isinstance(compas_geometry, CLine):
            return LineString(
                [
                    (
                        compas_geometry.start.x * config.css_pixel,
                        compas_geometry.start.y * config.css_pixel,
                    ),
                    (
                        compas_geometry.end.x * config.css_pixel,
                        compas_geometry.end.y * config.css_pixel,
                    ),
                ]
            )
        elif isinstance(compas_geometry, CPolyline):
            return LineString(
                [
                    (point.x * config.css_pixel, point.y * config.css_pixel)
                    for point in compas_geometry
                ]
            )
        elif isinstance(compas_geometry, CPoint):
            # TODO: radius exagerated for now. later smaller or pass ?
            return circle(
                compas_geometry.x * config.css_pixel,
                compas_geometry.y * config.css_pixel,
                10,
            )
        else:
            raise ValueError("Unsupported Compas geometry type")

    def __convert_compas_to_vpype_lines(self, compas_geometries):
        """Convert a list of Compas geometries to a vpype LineCollection."""
        vpype_lines = LineCollection()
        for compas_geometry in compas_geometries:
            shapely_line = self.__convert_compas_to_shapely(compas_geometry)
            vpype_lines.append(shapely_line)
        return vpype_lines

    def _print_geometry(self, object, limit=69):
        repr_str = repr(object)[1:-2]
        if len(repr_str) > limit:
            config.logger.info(f"[ADD] {repr_str[:limit]}...")
        else:
            config.logger.info(f"[ADD] {repr_str}")
