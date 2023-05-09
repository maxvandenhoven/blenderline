import random

import bpy
import mathutils


class PathReference:
    """Reference to path object in scene."""

    def __init__(self, path_object: bpy.types.Object) -> None:
        """Create reference to path object in scene.

        Args:
            path_object (bpy.types.Object): path object in scene.
        """
        # Save object attributes
        self.path_object = path_object

    def sample(self) -> tuple[mathutils.Vector, mathutils.Vector, mathutils.Vector]:
        """Sample random location along the path and return location, normal vector in
            the x-y plane, and a normal vector in the local z plane.

        Returns:
            mathutils.Vector: location in global space. Used to position items.
            mathutils.Vector: normalized normal vector of the sampled location in the
                global x-y plane. Used to randomly move items laterally.
            mathutils.Vector: normalized normal vector of sampled location in the local z
                plane. Used to orient items upright for sloped paths.
        """
        # Get curve data from path object. It is assumed that path object only has one
        # curve, which in turn only has one spline. No error will be thrown otherwise,
        # but unexpected locations may be sampled.
        path_curve: bpy.types.Curve = self.path_object.data
        bezier_points = path_curve.splines[0].bezier_points

        # Curves consist of segments, which are defined between two control points. Each
        # segment adds 1 to the domain of t, the parameter defining a location on the
        # curve. For example, t=1.5 denotes the halfway mark of the second segment,
        # whereas t=0.5 denotes the halfway mark of the first segment.
        segment_index, t = divmod(random.random() * (len(bezier_points) - 1), 1)
        segment_index = int(segment_index)

        # Each segment is a cubic bezier curve, on which a point can be computed using the
        # explicit formula shown on wikipedia.
        p0: mathutils.Vector = bezier_points[segment_index].co
        p1: mathutils.Vector = bezier_points[segment_index].handle_right
        p2: mathutils.Vector = bezier_points[segment_index + 1].handle_left
        p3: mathutils.Vector = bezier_points[segment_index + 1].co
        location = (
            (1 - t) ** 3 * p0
            + 3 * t * (1 - t) ** 2 * p1
            + 3 * t**2 * (1 - t) * p2
            + t**3 * p3
        )

        # Compute location tangent by computing derivative of point using the explicit
        # formula shown on wikipedia.
        tangent = (
            3 * (1 - t) ** 2 * (p1 - p0)
            + 6 * t * (1 - t) * (p2 - p1)
            + 3 * t**2 * (p3 - p2)
        )
        tangent.normalize()

        # Compute normal to location by taking cross product of tangent line and z-vector.
        # This produces a normal vector in the x-y plane, which is used for lateral
        # offsetting of items on the path.
        normal_global_xy = tangent.cross(mathutils.Vector((0, 0, -1)))
        normal_global_xy.normalize()

        # Take cross product of tangent line and normal in the x-y plane to get normal to
        # location in the local z direction, which is used for orientation of items on
        # sloped paths.
        normal_local_z = tangent.cross(normal_global_xy)
        normal_local_z.normalize()

        return location, normal_global_xy, normal_local_z
