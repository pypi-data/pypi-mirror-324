import typing
import collections.abc
import typing_extensions
import bpy.types

def edge_face_count(mesh) -> list:
    """

    :return: list face users for each item in mesh.edges.
    :rtype: list
    """

def edge_face_count_dict(mesh) -> dict:
    """

        :return: dict of edge keys with their value set to the number of
    faces using each edge.
        :rtype: dict
    """

def edge_loops_from_edges(mesh, edges=None):
    """Edge loops defined by edgesTakes me.edges or a list of edges and returns the edge loopsreturn a list of vertex indices.
    [ [1, 6, 7, 2], ...]closed loops have matching start and end values.

    """

def mesh_linked_triangles(mesh: bpy.types.Mesh) -> list:
    """Splits the mesh into connected triangles, use this for separating cubes from
    other mesh elements within 1 mesh datablock.

        :param mesh: the mesh used to group with.
        :type mesh: bpy.types.Mesh
        :return: lists of lists containing triangles.
        :rtype: list
    """

def mesh_linked_uv_islands(mesh: bpy.types.Mesh) -> list:
    """Splits the mesh into connected polygons, use this for separating cubes from
    other mesh elements within 1 mesh datablock.

        :param mesh: the mesh used to group with.
        :type mesh: bpy.types.Mesh
        :return: lists of lists containing polygon indices
        :rtype: list
    """

def ngon_tessellate(
    from_data: bpy.types.Mesh | list,
    indices: list,
    fix_loops: bool = True,
    debug_print=True,
):
    """Takes a polyline of indices (fgon) and returns a list of face
    index lists. Designed to be used for importers that need indices for an
    fgon to create from existing verts.

        :param from_data: either a mesh, or a list/tuple of vectors.
        :type from_data: bpy.types.Mesh | list
        :param indices: a list of indices to use this list
    is the ordered closed polyline
    to fill, and can be a subset of the data given.
        :type indices: list
        :param fix_loops: If this is enabled polylines
    that use loops to make multiple
    polylines are delt with correctly.
        :type fix_loops: bool
    """

def triangle_random_points(
    num_points, loop_triangles: bpy.types.MeshLoopTriangle | collections.abc.Sequence
) -> list:
    """Generates a list of random points over mesh loop triangles.

    :param num_points: the number of random points to generate on each triangle.
    :param loop_triangles: list of the triangles to generate points on.
    :type loop_triangles: bpy.types.MeshLoopTriangle | collections.abc.Sequence
    :return: list of random points over all triangles.
    :rtype: list
    """
