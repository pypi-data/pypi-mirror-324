from .nodes import (
    LatticePointsNode,
    SphereArrayNode,
    CylinderArrayNode,
    UnionNode,
    BoundingBoxNode,
    BooleanDifferenceNode
)

def build_node_graph(n=4, spacing=1.0, sphere_radius=0.2, cylinder_radius=0.1):
    # 1. Lattice points
    points_node = LatticePointsNode(
        name="points_node",
        properties={
            "n": n,
            "spacing": spacing
        }
    )

    # 2. Spheres
    spheres_node = SphereArrayNode(
        name="spheres_node",
        inputs={"points": points_node},
        properties={"radius": sphere_radius}
    )

    # 3. Cylinders
    cylinders_node = CylinderArrayNode(
        name="cylinders_node",
        inputs={"points": points_node},
        properties={
            "radius": cylinder_radius,
            "n": n,
            "spacing": spacing
        }
    )

    # 4. Union of spheres + cylinders
    union_node = UnionNode(
        name="union_node",
        inputs={
            "objects": [spheres_node, cylinders_node]
        }
    )

    # 5. Bounding box
    bbox_node = BoundingBoxNode(
        name="bbox_node",
        properties={
            "n": n,
            "spacing": spacing
        }
    )

    # 6. Difference
    diff_node = BooleanDifferenceNode(
        name="diff_node",
        inputs={
            "base": bbox_node,
            "tool": union_node
        }
    )

    final_geom = diff_node.get_output()
    return final_geom
