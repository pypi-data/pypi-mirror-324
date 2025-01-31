# Design-of-porous-structures

A **node-based CadQuery library** for generating a simple cubic lattice (spheres + cylinders) inside a bounding box.  
This project was developed in Jupyter and packaged as a Python library.

## Features
- Node classes (spheres, cylinders, bounding box, booleans)
- Parametric design (adjust `n`, `spacing`, etc.)
- Uses CadQuery for robust CSG operations

## Installation

**Method 1: Local Install**

1. Download or clone this repo.
2. In a terminal (or Jupyter with `!` magic), do:
   ```bash
   pip install .
3. Ensure you have CadQuery >= 2.1.0 installed.


## Usage Example

import cadquery as cq
from my_lattice_graph import build_node_graph

model = build_node_graph(n=4, spacing=1.0, sphere_radius=0.2, cylinder_radius=0.1)
cq.exporters.export(model, "my_lattice_output.step")
cq.exporters.export(model, "my_lattice_output.stl")