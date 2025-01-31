import cadquery as cq
import numpy as np

class Node:
    def __init__(self, name, inputs=None, properties=None):
        """
        :param name: A unique name/identifier for this node.
        :param inputs: Dict of named inputs, e.g. {"geometry": some_other_node}.
        :param properties: Dict of parameter values for the node.
        """
        self.name = name
        self.inputs = inputs if inputs else {}
        self.properties = properties if properties else {}
        self._cached_output = None

    def evaluate(self):
        raise NotImplementedError("Subclasses must implement evaluate()")

    def get_output(self):
        if self._cached_output is None:
            self._cached_output = self.evaluate()
        return self._cached_output

    def invalidate_cache(self):
        self._cached_output = None


class LatticePointsNode(Node):
    def evaluate(self):
        n = self.properties.get("n", 4)
        spacing = self.properties.get("spacing", 1.0)

        points = np.array([
            (x, y, z)
            for x in range(n)
            for y in range(n)
            for z in range(n)
        ]) * spacing
        return points


class SphereArrayNode(Node):
    def evaluate(self):
        points_node = self.inputs.get("points")
        sphere_radius = self.properties.get("radius", 0.2)

        points = points_node.get_output()
        model = cq.Workplane("XY")
        for pt in points:
            model = model.union(
                cq.Workplane("XY")
                .sphere(sphere_radius)
                .translate(tuple(pt))  # tuple() fix
            )
        return model


class CylinderArrayNode(Node):
    def evaluate(self):
        points_node = self.inputs.get("points")
        cylinder_radius = self.properties.get("radius", 0.1)
        n = self.properties.get("n", 4)
        spacing = self.properties.get("spacing", 1.0)

        points = points_node.get_output()

        # Build adjacency for simple cubic
        connections = []
        for x in range(n):
            for y in range(n):
                for z in range(n):
                    idx = x*n*n + y*n + z
                    if x < n - 1:
                        connections.append((idx, idx + n*n))
                    if y < n - 1:
                        connections.append((idx, idx + n))
                    if z < n - 1:
                        connections.append((idx, idx + 1))

        model = cq.Workplane("XY")
        for start, end in connections:
            start_pt = points[start]
            end_pt = points[end]
            vec = end_pt - start_pt
            height = np.linalg.norm(vec)
            if height < 1e-9:
                continue

            z_axis = np.array([0,0,1])
            axis = np.cross(z_axis, vec)
            axis_len = np.linalg.norm(axis)
            if axis_len < 1e-9:
                axis = z_axis
                angle = 0
            else:
                angle = np.degrees(
                    np.arccos(
                        np.clip(np.dot(z_axis, vec)/height, -1.0, 1.0)
                    )
                )

            midpoint = 0.5 * (start_pt + end_pt)

            cyl = (
                cq.Workplane("XY")
                .cylinder(height, cylinder_radius)
                .rotate((0,0,0), tuple(axis), angle)
                .translate(tuple(midpoint))
            )
            model = model.union(cyl)

        return model


class UnionNode(Node):
    def evaluate(self):
        objects = self.inputs.get("objects", [])
        if not objects:
            return None

        result = None
        for obj_node in objects:
            geom = obj_node.get_output()
            if result is None:
                result = geom
            else:
                result = result.union(geom)
        return result


class BoundingBoxNode(Node):
    def evaluate(self):
        n = self.properties.get("n", 4)
        spacing = self.properties.get("spacing", 1.0)
        side = (n - 1) * spacing

        box = cq.Workplane("XY").box(side, side, side, centered=(False,False,False))
        return box


class BooleanDifferenceNode(Node):
    def evaluate(self):
        base_node = self.inputs.get("base")
        tool_node = self.inputs.get("tool")

        base_geom = base_node.get_output()
        tool_geom = tool_node.get_output()

        return base_geom.cut(tool_geom)
