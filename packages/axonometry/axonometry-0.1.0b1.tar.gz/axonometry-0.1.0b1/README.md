<!--
SPDX-FileCopyrightText: 2024 Julien Rippinger

SPDX-License-Identifier: CC-BY-4.0
-->

[![REUSE status](https://api.reuse.software/badge/codeberg.org/mononym/axonometry)](https://api.reuse.software/info/codeberg.org/mononym/axonometry)
[![status-badge](https://ci.codeberg.org/api/badges/14144/status.svg?branch=beta)](https://ci.codeberg.org/repos/14144/branches/beta)

## Notes & Principles

+ 3D CGI matrix transformations use 4 [Homogeneous Coordinates](https://en.wikipedia.org/wiki/Homogeneous_coordinates) - we have 2D projections & use 3 Cartesian coordinates.
+ To play with projections quickly, the operations transform points to lines, lines to surfaces, surfaces to solids.
+ Prefer class methods for operations on a single Point|Line|Surface(polyline); use functions for operations on two or more objects.
+ Replace the observer design pattern with an operative data structure: tree (I think)
+ the graphical primitive most often handled by the user is the line: points are most often used to project orthogonal lines from them.
+ Fewer but more intuitive operations give more possibilities; think about [Affordances](https://monoskop.org/images/c/c6/Gibson_James_J_1977_1979_The_Theory_of_Affordances.pdf): a limited set of operations can enhance intuitive operations and expand the use cases.
+ Most operations leave traces and are recorded in order: making the drawing on a plotter re-enacts this order of construction.
+ Projective/geometric consistencies are not sought or enforced: projection operations are propagated, but these traces do not have to be consistent with existing or future geometry. Every object needs a minimum of projectional traces to be defined, but all the views are not necessarily updated.
+ A drawing is never finished, but only the beginning: the aim is not to generate full, glossy drawings in one click.
+ Lines are internally infinite, but rendered as segments.
+ compas is used for geometry, vpype for i/o; everything created is stored in a vpype document instance
+ Start coding in a venv installation; switch to conda if bugs appear
+ Python version 3.12, not above
+ Default paper size is A1, units are in mm (converted to CSS pixels for rendering in scale)
+ Prefer radians (internally)
+ Three ways of adding/projecting geometry:
  1. From the axonometry object: `Axonometry.add_*(<geometry>)`. The place to add the geometry is evaluated from the geometry. A Point(x,y,z) is added in the axonometric space. Point(x,y), Point(y,z) and Point(z,x) are added in their respective reference planes.
  2. Therefore, on can also add objects directly in a reference plane: `Axonometry[<reference_plane_key>].add_*(<geometry>)`
  3. One can also manipulate objects by their own methods (i.e. their parents are the planes they are in): `Point().project(<parameters>)`
+ Projecting an object always returns a new object

## Installation

```
git clone --branch beta git@codeberg.org:mononym/axonometry.git && cd axonometry
python -m venv venv
source venv/bin/activate
python -m pip install --upgrade pip
python -m pip install .
```

For development, replace the last line with `python -m pip install --editable .`

## TODO

+ What is the role of layers ?

## Milestones

+ Import existing SVG files and place them in the axonometry or one of the three coordinate planes.
+ Project lines and faces
+ auto-execute code (with vsketch)
