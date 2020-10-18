import numpy as np
from phonopy.structure.grid_points import GridPoints

ga234 = [[0, 0, 0],
         [1, 0, 0],
         [0, 1, 0],
         [1, 1, 0],
         [0, -1, 0],
         [-1, -1, 0],
         [0, 0, 1],
         [1, 0, 1],
         [0, 1, 1],
         [1, 1, 1],
         [0, -1, 1],
         [1, 2, 1],
         [0, 0, 2],
         [1, 0, 2],
         [0, 1, 2],
         [1, 1, 2],
         [0, -1, -2],
         [-1, -1, -2],
         [0, 0, -1],
         [-1, 0, -1],
         [0, 1, -1],
         [-1, -2, -1],
         [0, -1, -1],
         [-1, -1, -1]]


def test_GridPoints():
    gp = GridPoints([2, 3, 4], [[-1, 1, 1], [1, -1, 1], [1, 1, -1]])
    np.testing.assert_array_equal(gp.grid_address, ga234)


def test_GridPoints_with_rotations(ph_nacl):
    rec_lat = np.linalg.inv(ph_nacl.primitive.cell)
    rotations = ph_nacl.primitive_symmetry.get_pointgroup_operations()
    gp = GridPoints([4, 4, 4], rec_lat, rotations=rotations)
    np.testing.assert_array_equal(
        gp.ir_grid_points, [0, 1, 2, 5, 6, 7, 10, 27])
    np.testing.assert_array_equal(gp.weights, [1, 8, 4, 6, 24, 12, 3, 6])
    np.testing.assert_array_equal(
        gp.grid_mapping_table,
        [0, 1, 2, 1, 1, 5, 6, 7, 2, 6,
         10, 6, 1, 7, 6, 5, 1, 5, 6, 7,
         5, 1, 7, 6, 6, 7, 6, 27, 7, 6,
         27, 6, 2, 6, 10, 6, 6, 7, 6, 27,
         10, 6, 2, 6, 6, 27, 6, 7, 1, 7,
         6, 5, 7, 6, 27, 6, 6, 27, 6, 7,
         5, 6, 7, 1])
    np.testing.assert_allclose(
        gp.qpoints,
        [[0.0, 0.0, 0.0],
         [0.25, 0.0, 0.0],
         [0.5, 0.0, 0.0],
         [0.25, 0.25, 0.0],
         [0.5, 0.25, 0.0],
         [-0.25, 0.25, 0.0],
         [0.5, 0.5, 0.0],
         [-0.25, 0.5, 0.25]], atol=1e-8)


def test_GridPoints_with_rotations_fit_BZ_falase(ph_nacl):
    rec_lat = np.linalg.inv(ph_nacl.primitive.cell)
    rotations = ph_nacl.primitive_symmetry.get_pointgroup_operations()
    mesh = [5, 5, 5]
    gpf = GridPoints(mesh, rec_lat, rotations=rotations,
                     fit_in_BZ=False)
    gpt = GridPoints(mesh, rec_lat, rotations=rotations,
                     fit_in_BZ=True)
    np.testing.assert_allclose(
        gpf.qpoints,
        [[0.0, 0.0, 0.0],
         [0.2, 0.0, 0.0],
         [0.4, 0.0, 0.0],
         [0.2, 0.2, 0.0],
         [0.4, 0.2, 0.0],
         [-0.4, 0.2, 0.0],
         [-0.2, 0.2, 0.0],
         [0.4, 0.4, 0.0],
         [-0.4, 0.4, 0.0],
         [-0.4, 0.4, 0.2]], atol=1e-8)
    np.testing.assert_allclose(
        gpt.qpoints,
        [[0.0, 0.0, 0.0],
         [0.2, 0.0, 0.0],
         [0.4, 0.0, 0.0],
         [0.2, 0.2, 0.0],
         [0.4, 0.2, 0.0],
         [-0.4, 0.2, 0.0],
         [-0.2, 0.2, 0.0],
         [0.4, 0.4, 0.0],
         [-0.4, -0.6, 0.0],
         [0.6, 0.4, 0.2]], atol=1e-8)
