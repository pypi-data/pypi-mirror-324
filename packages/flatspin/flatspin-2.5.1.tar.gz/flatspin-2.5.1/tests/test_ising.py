import numpy as np
from numpy.linalg import norm
import itertools
import pytest
from .utils import approx, assert_allclose
from numpy.testing import assert_array_equal
from os import path
import pandas as pd

from flatspin import IsingSpinIce, CustomSpinIce
from flatspin.astroid import gsw_astroid, astroid_params
from flatspin.data import Dataset, save_table
from flatspin.utils import label_columns

def test_init(opencl):
    si = IsingSpinIce(size=(5,4), **opencl)
    N = 5 * 4

    assert si.size == (5, 4)
    assert si.num_neighbors == 4
    assert si.spin_count == N

    assert si.spin.shape == (N,)
    assert si.pos.shape == (N, 2)
    assert si.angle.shape == (N,)
    assert si.threshold.shape == (N,)
    assert si.m.shape == (N, 2)

    assert_array_equal(si.angle, np.pi/2) # spin dir is up

    expect = np.zeros(si.m.shape)
    expect[...,1] = 1
    assert_allclose(si.m, expect)

def test_label():
    si = IsingSpinIce(size=(3,2))

    assert si.label(0) == (0,0)
    assert si.label(1) == (0,1)
    assert si.label(2) == (0,2)
    assert si.label(3) == (1,0)
    assert si.label(4) == (1,1)
    assert si.label(5) == (1,2)

def test_labels():
    si = IsingSpinIce(size=(2,2))
    assert_array_equal(si.labels, [(0,0), (0,1), (1,0), (1,1)])

    si = IsingSpinIce(size=(3,2))
    assert_array_equal(si.labels, [(0,0), (0,1), (0,2), (1,0), (1,1), (1,2)])
    assert_array_equal(si.labels[[0,2,4]], [(0,0), (0,2), (1,1)])
    assert_array_equal(si.labels[1::2], [(0,1), (1,0), (1,2)])

def test_indexof():
    si = IsingSpinIce(size=(3,2))

    inds = [si.indexof(tuple(l)) for l in si.labels]
    assert_array_equal(inds, si.indices())

    # row 1
    assert_array_equal(si.indexof(1), [3, 4, 5])

    # col 1
    assert_array_equal(si.indexof((slice(None), 1)), [1, 4])

    # every other column
    assert_array_equal(si.indexof((slice(None), slice(0, None, 2))), [0, 2, 3, 5])

def test_randomize():
    seed = 0x1234321
    si = IsingSpinIce(size=(10,10), random_seed=seed)

    assert np.all(si.spin == 1)

    si.randomize()

    assert not np.all(si.spin == 1)
    assert not np.all(si.spin == -1)
    assert np.all(np.isin(si.spin, (-1,1)))

    spin0 = si.spin.copy()
    si.randomize()
    assert not np.all(si.spin == spin0)

    si.randomize(seed=seed)
    assert np.all(si.spin == spin0)

def test_total_fields_single(opencl):
    si = IsingSpinIce(size=(1,1), **opencl)
    si.randomize()

    h_tot = si.total_fields()
    for i in si.indices():
        assert tuple(h_tot[i]) == tuple(si.total_field(i))

def test_dipolar_fields_single(opencl):
    si = IsingSpinIce(size=(1,1), **opencl)
    si.randomize()

    h_dip = si.dipolar_fields()
    for i in si.indices():
        assert tuple(h_dip[i]) == tuple(si.dipolar_field(i))

def test_L():
    si = IsingSpinIce(size=(4,3))

    inds = list(si.L[tuple(i)] for i in si.labels)

    assert_array_equal(inds, si.indices())

    assert si.L[0,0] == 0
    assert si.L[0,1] == 1
    assert si.L[0,2] == 2
    assert si.L[0,3] == 3
    assert si.L[1,0] == 4
    assert si.L[1,1] == 5
    assert si.L[1,2] == 6
    assert si.L[1,3] == 7
    assert si.L[2,0] == 8
    assert si.L[2,1] == 9
    assert si.L[2,2] == 10
    assert si.L[2,3] == 11

    # row 1
    assert_array_equal(si.L[1], [4, 5, 6, 7])

    # col 1
    assert_array_equal(si.L[:,1], [1, 5, 9])

    # rows 1:2
    assert_array_equal(si.L[1:3], [4, 5, 6, 7, 8, 9, 10, 11])

    # cols 2:3
    assert_array_equal(si.L[:,2:4], [2, 3, 6, 7, 10, 11])

    # every other row
    assert_array_equal(si.L[::2], [0, 1, 2, 3, 8, 9, 10, 11])

    # every other column
    assert_array_equal(si.L[:,::2], [0, 2, 4, 6, 8, 10])

    # rows 1:2, cols 2:3
    assert_array_equal(si.L[1:3,2:4], [6, 7, 10, 11])

    # rows 0 and 2
    assert_array_equal(si.L[[0,2]], [0, 1, 2, 3, 8, 9, 10, 11])

    # columns 1 and 3
    assert_array_equal(si.L[:,[1,3]], [1, 3, 5, 7, 9, 11])

    # last row
    assert_array_equal(si.L[-1], [8, 9, 10, 11])

    # last column
    assert_array_equal(si.L[:,-1], [3, 7, 11])

def test_pos():
    si = IsingSpinIce(size=(2,3))
    expect = [[0,0], [1,0], [0,1], [1,1], [0,2], [1,2]]
    assert_array_equal(si.pos, expect)

def test_lattice_spacing():
    L = np.pi
    si = IsingSpinIce(size=(2,3), lattice_spacing=L)
    expect = L * np.array([[0,0], [1,0], [0,1], [1,1], [0,2], [1,2]])
    assert_array_equal(si.pos, expect)

def test_threshold():
    # No disorder
    hc = 0.0142
    si = IsingSpinIce(size=(101,102), hc=hc)

    assert si.hc == hc
    assert_array_equal(si.threshold, hc)

    # With disorder
    hc = 0.1
    disorder = 0.3
    si = IsingSpinIce(size=(70,80), hc=hc, disorder=disorder)

    assert si.hc == hc
    assert np.mean(si.threshold) == approx(hc, abs=1e-2)
    assert np.std(si.threshold) == approx(disorder * hc, abs=1e-3)

    # make sure we don't have negative thresholds
    si = IsingSpinIce(size=(100,100), hc=1, disorder=100)

    assert np.count_nonzero(si.threshold < 0) == 0

def test_threshold_grid():
    # No disorder
    hc = np.array(
        [[0.1, 0.2, 0.3],
         [0.4, 0.5, 0.6]]
    )
    si = IsingSpinIce(size=(63,92), hc=hc)

    assert_array_equal(si.hc, hc)

    grid = si.fixed_grid((hc.shape[1], hc.shape[0]))
    for p in np.ndindex(grid.size):
        inds = grid.point_index(p)
        assert_array_equal(si.threshold[inds], hc[p])

    # With disorder
    disorder = 0.04
    si = IsingSpinIce(size=(103,97), hc=hc, disorder=disorder)

    assert_array_equal(si.hc, hc)

    grid = si.fixed_grid((hc.shape[1], hc.shape[0]))
    for p in np.ndindex(grid.size):
        inds = grid.point_index(p)
        assert np.mean(si.threshold[inds]) == approx(hc[p], abs=1e-2)
        assert np.std(si.threshold[inds]) == approx(disorder * hc[p], abs=1e-3)

    # make sure we don't have negative thresholds
    si = IsingSpinIce(size=(91,123), hc=hc, disorder=100)
    assert np.count_nonzero(si.threshold < 0) == 0

def test_set_hc():
    # No disorder
    hc = 0.0123
    si = IsingSpinIce(size=(100,100), hc=hc)

    assert si.hc == hc
    assert_array_equal(si.threshold, hc)

    hc = 0.0333
    si.set_hc(hc)
    assert si.hc == hc
    assert_array_equal(si.threshold, hc)

    # With disorder
    hc = 0.1
    disorder = 0.3
    si = IsingSpinIce(size=(100,100), hc=hc, disorder=disorder)

    assert si.hc == hc
    assert np.mean(si.threshold) == approx(hc, abs=1e-2)
    assert np.std(si.threshold) == approx(disorder * hc, abs=1e-3)

    old_hc = si.hc
    old_threshold = si.threshold.copy()
    hc = 0.2
    si.set_hc(hc)
    assert si.hc == hc
    assert np.mean(si.threshold) == approx(hc, abs=1e-2)
    assert np.std(si.threshold) == approx(disorder * hc, abs=1e-3)

    # Test that the new thresholds retain the distribution of the old thresholds
    assert si.threshold == approx(old_threshold * hc / old_hc)

    # no grid -> no grid
    #   no need to invoke grid
    # no grid -> grid
    #   call set_hc_grid()
    # grid -> grid
    #   call set_hc_grid()
    # grid -> no grid
    #   call set_hc_grid()

@pytest.mark.parametrize("switching", ["budrikis", "sw"])
def test_set_hc_flippable(opencl, switching):
    si = IsingSpinIce(
        size=(4,4), alpha=0, hc=1.0, sw_b=1, spin_angle=0,
        neighbor_distance=np.inf, switching=switching, **opencl)

    # Apply field along easy axis, stronger than hc, all spins should flip
    si.set_h_ext([-1.1, 0])
    assert len(si.flippable()) == si.spin_count

    # Weaker than hc, no flips
    si.set_h_ext([-.9, 0])
    assert len(si.flippable()) == 0

    # Reduce hc below h_ext, all spins should flip
    si.set_hc(.8)
    assert len(si.flippable()) == si.spin_count

def test_set_hc_grid():
    # No disorder
    hc = np.array(
        [[0.1, 0.2, 0.3],
         [0.4, 0.5, 0.6]]
    )
    si = IsingSpinIce(size=(32, 23))

    # no grid -> grid
    si.set_hc(hc)

    grid = si.fixed_grid((hc.shape[1], hc.shape[0]))
    for p in np.ndindex(grid.size):
        inds = grid.point_index(p)
        assert_array_equal(si.threshold[inds], hc[p])

    # grid -> grid
    hc = np.array(
        [[0.3, 0.1, 0.02]]
    )
    si.set_hc(hc)

    grid = si.fixed_grid((hc.shape[1], hc.shape[0]))
    for p in np.ndindex(grid.size):
        inds = grid.point_index(p)
        assert_array_equal(si.threshold[inds], hc[p])

    # grid -> no grid
    hc = 0.132
    si.set_hc(hc)
    assert_array_equal(si.threshold, hc)


    # With disorder
    hc = np.array(
        [[0.1, 0.2, 0.3],
         [0.4, 0.5, 0.6]]
    )
    disorder = 0.05
    si = IsingSpinIce(size=(132, 123), disorder=disorder)

    # no grid -> grid
    old_hc = si.hc
    old_threshold = si.threshold.copy()
    si.set_hc(hc)

    grid = si.fixed_grid((hc.shape[1], hc.shape[0]))
    for p in np.ndindex(grid.size):
        inds = grid.point_index(p)
        assert np.mean(si.threshold[inds]) == approx(hc[p], abs=1e-2)
        assert np.std(si.threshold[inds]) == approx(disorder * hc[p], abs=1e-3)
        assert si.threshold[inds] == approx(old_threshold[inds] * hc[p] / old_hc)

    # grid -> grid
    hc = np.array(
        [[0.3, 0.1, 0.02],
         [0.6, 0.5, 0.4]]
    )
    si.set_hc(hc)

    grid = si.fixed_grid((hc.shape[1], hc.shape[0]))
    for p in np.ndindex(grid.size):
        inds = grid.point_index(p)
        assert np.mean(si.threshold[inds]) == approx(hc[p], abs=1e-2)
        assert np.std(si.threshold[inds]) == approx(disorder * hc[p], abs=1e-3)
        assert si.threshold[inds] == approx(old_threshold[inds] * hc[p] / old_hc)

    # grid -> no grid
    hc = 0.132
    si.set_hc(hc)
    assert np.mean(si.threshold) == approx(hc, abs=1e-2)
    assert np.std(si.threshold) == approx(disorder * hc, abs=1e-3)
    assert si.threshold == approx(old_threshold * hc / old_hc)

def test_set_hc_direct():
    ## no disorder
    # init_scalar -> direct -> scalar
    si = IsingSpinIce(size=(32, 23))
    hc = [i + 1 for i in range(si.spin_count)]
    si.set_hc(hc)
    assert_array_equal(si.threshold, hc)
    assert_array_equal(si.hc, hc)
    assert  isinstance(si.hc, np.ndarray)

    hc = 1.337
    si.set_hc(hc)
    assert_allclose(si.threshold, np.full(si.spin_count, hc))
    assert si.hc == hc
    assert np.isscalar(si.hc)

    # init_direct -> scalar -> direct
    hc = [1 + (1/3) * i for i in range(si.spin_count)]
    si = IsingSpinIce(size=(32, 23), hc=hc)
    assert_array_equal(si.threshold, hc)
    assert_array_equal(si.hc, hc)
    assert  isinstance(si.hc, np.ndarray)

    hc = 0.1
    si.set_hc(hc)
    assert_allclose(si.threshold, np.full(si.spin_count, hc))
    assert si.hc == hc
    assert np.isscalar(si.hc)

    hc = np.arange(si.spin_count) + np.pi
    si.set_hc(hc)
    assert_allclose(si.threshold, hc)
    assert_array_equal(si.hc, hc)
    assert  isinstance(si.hc, np.ndarray)

    # init_grid -> direct -> grid
    hc = [[1,2,3],[4,5,6]]
    si = IsingSpinIce(size=(11, 19), hc=hc)

    hc = [1 + i*0.5 for i in range(si.spin_count)]
    si.set_hc(hc)
    assert_array_equal(si.threshold, hc)
    assert_array_equal(si.hc, hc)
    assert  isinstance(si.hc, np.ndarray)

    hc = [[1,1,2],[3,5,8],[13,21,34]]
    si.set_hc(hc)
    grid = si.fixed_grid((np.shape(hc)[1], np.shape(hc)[0]))
    for p in np.ndindex(grid.size):
        inds = grid.point_index(p)
        assert_allclose(si.threshold[inds], np.array(hc)[p])

    # init_direct -> grid -> direct
    hc = [2 + i for i in range(32 * 23)]
    si = IsingSpinIce(size=(32, 23), hc=hc)

    hc = [[1,np.pi]]
    si.set_hc(hc)
    grid = si.fixed_grid((np.shape(hc)[1], np.shape(hc)[0]))
    for p in np.ndindex(grid.size):
        inds = grid.point_index(p)
        assert_allclose(si.threshold[inds], np.array(hc)[p])

    hc = [1 + i for i in range(si.spin_count)]
    si.set_hc(hc)
    assert_allclose(si.threshold, hc)
    assert_array_equal(si.hc, hc)
    assert  isinstance(si.hc, np.ndarray)

    ## with disorder
    dis = 0.5
    # init_scalar -> direct -> scalar
    hc = 1
    si = IsingSpinIce(size=(32, 23), disorder=dis, hc=hc)
    raw_disorder = si.threshold / hc
    hc = [i + 1 for i in range(si.spin_count)]
    si.set_hc(hc)
    assert_array_equal(si.threshold, hc * raw_disorder)
    assert_array_equal(si.hc, hc)
    assert  isinstance(si.hc, np.ndarray)

    hc = 1.337
    si.set_hc(hc)
    assert_allclose(si.threshold, np.full(si.spin_count, hc) * raw_disorder)
    assert si.hc == hc
    assert np.isscalar(si.hc)

    # init_direct -> scalar -> direct
    hc = [1 + (1/3) * i for i in range(si.spin_count)]
    si = IsingSpinIce(size=(32, 23), disorder=dis, hc=hc)
    raw_disorder = si.threshold / hc
    assert_allclose(si.threshold, hc * raw_disorder)
    assert_array_equal(si.hc, hc)
    assert  isinstance(si.hc, np.ndarray)

    hc = 0.1
    si.set_hc(hc)
    assert_allclose(si.threshold, np.full(si.spin_count, hc) * raw_disorder)
    assert si.hc == hc
    assert np.isscalar(si.hc)

    hc = np.arange(si.spin_count) + np.pi
    si.set_hc(hc)
    assert_allclose(si.threshold, hc * raw_disorder)
    assert_array_equal(si.hc, hc)
    assert  isinstance(si.hc, np.ndarray)

    # init_grid -> direct -> grid
    hc = [[1,2,3],[4,5,6]]
    si = IsingSpinIce(size=(11, 19), disorder=dis, hc=hc)

    spin_hc = np.zeros(si.N)
    grid = si.fixed_grid((np.shape(hc)[1], np.shape(hc)[0]))
    grid_inds = grid.grid_index(np.arange(si.N))
    spin_hc[:] = np.array(hc)[grid_inds]
    raw_disorder = si.threshold / spin_hc

    hc = [1 + i*0.5 for i in range(si.spin_count)]
    si.set_hc(hc)
    assert_allclose(si.threshold, hc * raw_disorder)
    assert_array_equal(si.hc, hc)
    assert  isinstance(si.hc, np.ndarray)

    hc = [[1,1,2],[3,5,8],[13,21,34]]
    si.set_hc(hc)
    grid = si.fixed_grid((np.shape(hc)[1], np.shape(hc)[0]))
    assert_allclose(si.threshold, si.map_values_to_grid(hc) * raw_disorder)
    # init_direct -> grid -> direct
    hc = [2 + i for i in range(32 * 23)]
    si = IsingSpinIce(size=(32, 23), disorder=dis, hc=hc)
    raw_disorder = si.threshold / hc

    hc = [[1,np.pi]]
    si.set_hc(hc)
    grid = si.fixed_grid((np.shape(hc)[1], np.shape(hc)[0]))
    assert_allclose(si.threshold, si.map_values_to_grid(hc) * raw_disorder)

    hc = [1 + i for i in range(si.spin_count)]
    si.set_hc(hc)
    assert_allclose(si.threshold, hc * raw_disorder)
    assert_array_equal(si.hc, hc)
    assert  isinstance(si.hc, np.ndarray)





def test_set_threshold():
    # No disorder
    hc = 0.0123
    si = IsingSpinIce(size=(4, 4), hc=hc)

    assert si.hc == hc
    assert_array_equal(si.threshold, hc)

    new_threshold = np.linspace(0.1, 1, si.spin_count)
    si.set_threshold(new_threshold)

    assert_array_equal(si.threshold, new_threshold)

@pytest.mark.parametrize("switching", ["budrikis", "sw"])
def test_set_threshold_flippable(opencl, switching):
    si = IsingSpinIce(
        size=(4,4), alpha=0, hc=1.0, sw_b=1, spin_angle=0,
        neighbor_distance=np.inf, switching=switching, **opencl)

    # Weaker than hc, no flips
    H = .9 * si.hc
    si.set_h_ext([-H, 0])
    assert len(si.flippable()) == 0

    # Change thresholds, some will be below ext field
    new_threshold = si.hc * np.linspace(0.8, 1, si.spin_count)
    si.set_threshold(new_threshold)

    # Expect the thresholds that are below H to flip
    expect_flip, = np.nonzero(new_threshold < H)
    assert_array_equal(si.flippable(), expect_flip)

def test_num_neighbors():
    # global neighborhood
    si = IsingSpinIce(size=(3,3), neighbor_distance=np.inf)
    assert si.num_neighbors == si.spin_count - 1

    # nearest neighborhood (default)
    si = IsingSpinIce(size=(3,3))
    assert si.num_neighbors == 4

    # nearest including diagonals
    si = IsingSpinIce(size=(3,3), neighbor_distance=np.sqrt(2))
    assert si.num_neighbors == 8

def test_neighbors():
    # global neighborhood
    si = IsingSpinIce(size=(3,3), neighbor_distance=np.inf)
    indices = set(si.indices())
    for i in indices:
        assert set(si.neighbors(i)) == (indices - set([i]))

    # nearest neighborhood (default)
    si = IsingSpinIce(size=(3,3))
    L = si.L
    assert set(si.neighbors(L[0,0])) == set([L[0,1], L[1,0]])
    assert set(si.neighbors(L[0,1])) == set([L[0,0], L[0,2], L[1,1]])
    assert set(si.neighbors(L[0,2])) == set([L[0,1], L[1,2]])
    assert set(si.neighbors(L[1,0])) == set([L[0,0], L[1,1], L[2,0]])
    assert set(si.neighbors(L[1,1])) == set([L[0,1], L[1,0], L[1,2], L[2,1]])
    assert set(si.neighbors(L[1,2])) == set([L[0,2], L[1,1], L[2,2]])
    assert set(si.neighbors(L[2,0])) == set([L[1,0], L[2,1]])
    assert set(si.neighbors(L[2,1])) == set([L[1,1], L[2,0], L[2,2]])
    assert set(si.neighbors(L[2,2])) == set([L[1,2], L[2,1]])


def test_spin_dipolar_field(opencl):
    # spins point up
    si = IsingSpinIce(size=(2,2), **opencl)
    L = si.L

    j_T = 1
    j_L = 2
    j_D = 1/(4*np.sqrt(2))

    # parallell spins
    assert si.spin_dipolar_field(L[0,0], L[0,1]) == approx([-j_T, 0])

    # aligned spins
    assert si.spin_dipolar_field(L[0,0], L[1,0]) == approx([j_L, 0])

    # 45 degree neighbors
    assert si.spin_dipolar_field(L[0,0], L[1,1]) == approx([j_D, -3*j_D])

def test_dipolar_field(opencl):
    si = IsingSpinIce(size=(2,2), alpha=1.0, neighbor_distance=np.inf, **opencl)
    L = si.L

    j_T = 1
    j_L = 2
    j_D = 1/(4*np.sqrt(2))

    assert si.dipolar_field(L[0,0]) == approx([-j_T + j_L + j_D, -3*j_D])
    si.flip(L[1,0])
    assert si.dipolar_field(L[0,0]) == approx([-j_T - j_L + j_D, -3*j_D])
    si.flip(L[0,0])
    assert si.dipolar_field(L[0,0]) == approx([j_T + j_L - j_D, 3*j_D])

    si = IsingSpinIce(size=(4,4), alpha=1.0, **opencl)

    for i in si.indices():
        tot = np.sum([si.spin_dipolar_field(i, j) for j in si.neighbors(i)], axis=0)
        assert tuple(si.dipolar_field(i)) == approx(tot)

def test_external_field(opencl):
    si = IsingSpinIce(size=(2,2), **opencl)
    L = si.L

    h_par, h_perp = si.external_field(L[0,0])
    assert h_par == h_perp == 0

    # global external field
    si.set_h_ext((0,1))
    h_par, h_perp = si.external_field(L[0,0])
    assert h_par == 1
    assert h_perp == approx(0)

    si.flip(L[0,0])
    assert si.external_field(L[0,0]) == approx([-1,0])

    si.set_h_ext((1,0))
    assert si.external_field(L[0,0]) == approx([0,1])

    # local external field
    h_ext = [(0,1), (1,0),
             (0,2), (-2,0)]
    si.set_h_ext(h_ext)
    si.polarize()

    assert si.external_field(L[0,0]) == approx([1, 0])
    assert si.external_field(L[0,1]) == approx([0, -1])
    assert si.external_field(L[1,0]) == approx([2, 0])
    assert si.external_field(L[1,1]) == approx([0, 2])

def test_external_field_grid(opencl):
    si = IsingSpinIce(size=(2,2), **opencl)
    L = si.L

    # external field on a grid
    h_ext = [[(0,1), (1,0)],
             [(0,2), (-2,0)]]
    si.set_h_ext_grid(h_ext)

    assert si.external_field(L[0,0]) == approx([1, 0])
    assert si.external_field(L[0,1]) == approx([0, -1])
    assert si.external_field(L[1,0]) == approx([2, 0])
    assert si.external_field(L[1,1]) == approx([0, 2])

def test_total_field(opencl):
    si = IsingSpinIce(size=(4,4), **opencl)
    si.randomize()

    # global external field
    si.set_h_ext((0,1))

    i = si.L[2,2]
    assert tuple(si.total_field(i)) == tuple(si.dipolar_field(i) + si.external_field(i))

    # local external field
    h_ext = np.zeros((si.spin_count, 2))
    h_ext[i] = [0,2]
    si.set_h_ext(h_ext)
    assert tuple(si.total_field(i)) == tuple(si.dipolar_field(i) + si.external_field(i))

def test_dipolar_fields(opencl):
    si = IsingSpinIce(size=(5,7), **opencl)
    si.randomize()

    h_dip = si.dipolar_fields()
    for i in si.indices():
        assert tuple(h_dip[i]) == tuple(si.dipolar_field(i))

def test_external_fields(opencl):
    si = IsingSpinIce(size=(3,9), **opencl)
    si.randomize()

    # global external field
    si.set_h_ext((2,5))

    h_ext = si.external_fields()
    for i in si.indices():
        assert tuple(h_ext[i]) == approx(tuple(si.external_field(i)))

    # local external field
    h_ext = np.random.uniform(-10, 10, (si.spin_count, 2))
    si.set_h_ext(h_ext)

    h_ext = si.external_fields()
    for i in si.indices():
        assert tuple(h_ext[i]) == approx(tuple(si.external_field(i)))

def test_total_fields(opencl):
    si = IsingSpinIce(size=(1,15), **opencl)
    si.randomize()

    # global external field
    si.set_h_ext((0,1))

    h_tot = si.total_fields()
    h_dip = si.dipolar_fields()
    h_ext = si.external_fields()
    assert_array_equal(h_tot, h_ext + h_dip)

    # local external field
    h_ext = np.random.uniform(-10, 10, (si.spin_count, 2))
    si.set_h_ext(h_ext)

    h_tot = si.total_fields()
    h_dip = si.dipolar_fields()
    h_ext = si.external_fields()
    assert_allclose(h_tot, h_ext + h_dip, 6)

@pytest.mark.parametrize("switching", ["budrikis", "sw"])
def test_flippable(opencl, switching):
    si = IsingSpinIce(size=(4,4), alpha=1.0, hc=1.0, sw_b=1, neighbor_distance=np.inf, switching=switching, **opencl)
    L = si.L
    assert len(si.flippable()) == 0
    si.flip(L[0,0])
    expected = [L[0,0]]
    assert_array_equal(si.flippable(), expected)

@pytest.mark.parametrize("switching", ["budrikis", "sw"])
def test_alpha(opencl, switching):
    hc = 1.0
    h_ext = -(hc + 2)
    si = IsingSpinIce(size=(4,4), alpha=1.0, hc=hc, h_ext=(0, h_ext), switching=switching, **opencl)
    h_dip = si.dipolar_fields()
    h_external = si.external_fields()
    h_tot = si.total_fields()
    n_flip = len(si.flippable())

    assert 0 < n_flip < si.spin_count

    # adjust alpha only
    alpha = 0.5
    si.set_alpha(alpha)

    assert_array_equal(si.dipolar_fields(), alpha * h_dip)
    assert_array_equal(si.external_fields(), h_external)
    assert_array_equal(si.total_fields(), alpha * h_dip + h_external)

    # adjust alpha, rescale hc and h_ext
    alpha = 0.5
    hc *= alpha
    h_ext *= alpha
    si = IsingSpinIce(size=(4,4), hc=hc, h_ext=(0, h_ext), alpha=alpha, switching=switching, **opencl)

    assert_array_equal(si.dipolar_fields(), alpha * h_dip)
    assert_array_equal(si.total_fields(), alpha * h_tot)
    assert len(si.flippable()) == n_flip

@pytest.mark.parametrize("switching", ["budrikis", "sw"])
def test_step(opencl, switching):
    si = IsingSpinIce(size=(4,4), alpha=1.0, hc=1.0, sw_b=1, neighbor_distance=np.inf, switching=switching, **opencl)
    si.flip(0)
    assert len(si.flippable()) == 1
    assert si.step()
    assert len(si.flippable()) == 0

@pytest.mark.parametrize("switching", ["budrikis", "sw"])
def test_relax(opencl, switching):
    si = IsingSpinIce(size=(8,8), alpha=1.0, hc=1.0, neighbor_distance=np.inf, switching=switching, **opencl)
    L = si.L
    assert si.relax() == 0
    si.flip(L[0,0])
    si.flip(L[0,1])
    assert si.relax() == 2
    assert len(si.flippable()) == 0

def test_relax_single(opencl):
    #if "use_cuda" in opencl:
    #    pytest.skip("test breaks subsequent cuda calls (memory corruption?)")

    si = IsingSpinIce(size=(1,1), alpha=1.0, hc=1.0, neighbor_distance=np.inf, **opencl)
    L = si.L
    assert si.relax() == 0
    si.set_h_ext((0,-1))
    assert si.relax() == 1
    assert len(si.flippable()) == 0

def test_energy(opencl):
    si = IsingSpinIce(size=(4,4), hc=1.0, **opencl)
    E0 = si.energy()
    si.flip(0)
    E1 = si.energy()
    assert E1[0] > E0[0]

@pytest.mark.parametrize("switching", ["budrikis", "sw"])
def test_total_energy(opencl, switching):
    si = IsingSpinIce(size=(6,5), hc=1.0, neighbor_distance=np.inf, switching=switching, **opencl)

    E = si.total_energy()
    si.flip(0)
    assert si.total_energy() > E

    si.randomize()
    E = si.total_energy()
    while si.step():
        assert si.total_energy() < E
        E = si.total_energy()

def test_vectors():
    si = IsingSpinIce(size=(4,2))
    spin = [1,  1, 1, -1,
            1, -1, -1, 1]
    si.set_spin(spin)

    # grid_spacing == lattice_spacing
    vectors = si.vectors
    expect = [[0,1], [0,1],  [0, 1], [0,-1],
              [0,1], [0,-1], [0,-1], [0, 1]]
    assert_allclose(vectors, expect)

def test_find_vertices():
    si = IsingSpinIce(size=(2,3))
    L = si.L
    vi, vj, indices = si.find_vertices()

    assert_array_equal(vi, [0, 0, 1, 1])
    assert_array_equal(vj, [0, 1, 0, 1])

    assert tuple(indices[0]) == (L[0,0], L[1,0])
    assert tuple(indices[1]) == (L[0,1], L[1,1])
    assert tuple(indices[2]) == (L[1,0], L[2,0])
    assert tuple(indices[3]) == (L[1,1], L[2,1])

def test_vertices():
    si = IsingSpinIce(size=(2,3))
    L = si.L
    indices = si.vertices()
    assert_array_equal(indices,
        [[L[0,0], L[1,0]],
         [L[0,1], L[1,1]],
         [L[1,0], L[2,0]],
         [L[1,1], L[2,1]]])

def test_vertex_indices():
    si = IsingSpinIce(size=(2,3))
    indices = np.transpose(si.vertex_indices())
    assert_array_equal(indices, [(0,0), (0,1), (1,0), (1,1)])

def test_vertex_type():
    si = IsingSpinIce(size=(4,2))
    spin = [1, -1, 1, -1,
            1, -1, -1, 1]
    si.set_spin(spin)

    vertex = si.vertices()

    assert si.vertex_type(vertex[0]) == 1
    assert si.vertex_type(vertex[1]) == 1
    assert si.vertex_type(vertex[2]) == 2
    assert si.vertex_type(vertex[3]) == 2

def test_vertex_pos():
    si = IsingSpinIce(size=(3,3))

    vertex = si.vertices()

    assert tuple(si.vertex_pos(vertex[0])) == (0, 0.5)
    assert tuple(si.vertex_pos(vertex[1])) == (1, 0.5)
    assert tuple(si.vertex_pos(vertex[2])) == (2, 0.5)
    assert tuple(si.vertex_pos(vertex[3])) == (0, 1.5)
    assert tuple(si.vertex_pos(vertex[4])) == (1, 1.5)
    assert tuple(si.vertex_pos(vertex[5])) == (2, 1.5)

def test_vertex_count():
    si = IsingSpinIce(size=(4,2))
    spin = [1, -1, -1, -1,
            1, -1, -1, 1]
    si.set_spin(spin)

    types, counts = si.vertex_count()
    assert_array_equal(types, [1, 2])
    assert_array_equal(counts, [3, 1])

def test_vertex_population():
    si = IsingSpinIce(size=(4,2))
    spin = [1, -1, 1, -1,
            1, -1, -1, 1]
    si.set_spin(spin)

    types, pops = si.vertex_population()
    assert_array_equal(types, [1, 2])
    assert_array_equal(pops, [0.5, 0.5])

def test_vertex_mag():
    si = IsingSpinIce(size=(4,2))
    spin = [1, -1, 1, -1,
            1, -1, -1, 1]
    si.set_spin(spin)

    vertex = si.vertices()

    assert_allclose(si.vertex_mag(vertex[0]), [0, 2])
    assert_allclose(si.vertex_mag(vertex[1]), [0, -2])
    assert_allclose(si.vertex_mag(vertex[2]), [0, 0])
    assert_allclose(si.vertex_mag(vertex[3]), [0, 0])

def test_spin_grid():
    si = IsingSpinIce(size=(4,2))
    spin = [1,  1, 1, -1,
            1, -1, -1, 1]
    si.set_spin(spin)

    assert si.lattice_spacing == 1

    # grid_spacing == lattice_spacing
    grid = si.spin_grid()
    assert grid.shape == (2, 4, 2)
    expect = [[[0,1], [0,1],  [0, 1], [0,-1]],
              [[0,1], [0,-1], [0,-1], [0, 1]]]
    assert_allclose(grid, expect)

    # grid_spacing < lattice_spacing
    grid = si.spin_grid(0.5)
    assert grid.shape == (3, 7, 2)
    expect = [[[0,1], [0,0], [0, 1], [0,0], [0, 1], [0,0], [0,-1]],
              [[0,0], [0,0], [0, 0], [0,0], [0, 0], [0,0], [0, 0]],
              [[0,1], [0,0], [0,-1], [0,0], [0,-1], [0,0], [0, 1]]]
    assert_allclose(grid, expect)

    # grid_spacing > lattice_spacing
    grid = si.spin_grid(2.0)
    assert grid.shape == (1, 2, 2)
    expect = [[[0,2], [0,0]]]
    assert_allclose(grid, expect)

    # sum of all spins
    grid = si.spin_grid(4.0)
    assert grid.shape == (1, 1, 2)
    expect = [[[0,2]]]
    assert_allclose(grid, expect)

def test_grid():
    si = IsingSpinIce(size=(4,4))
    L = si.L

    assert si.lattice_spacing == 1

    #
    # default grid fits perfectly
    #
    grid = si.grid()
    assert grid.cell_size == (1, 1)
    assert grid.size == (4, 4)

    assert grid.grid_index(L[0,0]) == (0,0)
    spin_indices = si.all_indices()
    grid_indices = grid.grid_index(spin_indices)
    assert_array_equal(grid_indices, np.transpose(si.labels))


    #
    # cell_size 2x2 evenly divides lattice spacing
    #
    grid = si.grid(cell_size=2)
    assert grid.cell_size == (2, 2)
    assert grid.size == (2, 2)

    # cell (0,0)
    i = [L[0,0], L[0,1], L[1,0], L[1,1]]
    gi = grid.grid_index(i)
    assert np.all(np.transpose(gi) == [0,0])
    assert_array_equal(grid.point_index((0,0)), i)

    # cell (0,1)
    i = [L[0,2], L[0,3], L[1,2], L[1,3]]
    gi = grid.grid_index(i)
    assert np.all(np.transpose(gi) == [0,1])
    assert_array_equal(grid.point_index((0,1)), i)

    # cell (1,0)
    i = [L[2,0], L[2,1], L[3,0], L[3,1]]
    gi = grid.grid_index(i)
    assert np.all(np.transpose(gi) == [1,0])
    assert_array_equal(grid.point_index((1,0)), i)

    # cell (1,1)
    i = [L[2,2], L[2,3], L[3,2], L[3,3]]
    gi = grid.grid_index(i)
    assert np.all(np.transpose(gi) == [1,1])
    assert_array_equal(grid.point_index((1,1)), i)


    #
    # cell_size 3x2 does not evently divide lattice_spacing
    #
    grid = si.grid(cell_size=(3, 2))
    assert grid.cell_size == (3, 2)
    assert grid.size == (2, 2)

    # cell (0,0)
    i = [L[0,0], L[0,1], L[0,2], L[1,0], L[1,1], L[1,2]]
    pi = grid.point_index((0,0))
    assert_array_equal(pi, i)

    # cell (0,1)
    i = [L[0,3], L[1,3]]
    pi = grid.point_index((0,1))
    assert_array_equal(pi, i)

    # cell (1,0)
    i = [L[2,0], L[2,1], L[2,2], L[3,0], L[3,1], L[3,2]]
    pi = grid.point_index((1,0))
    assert_array_equal(pi, i)

    # cell (1,1)
    i = [L[2,3], L[3,3]]
    pi = grid.point_index((1,1))
    assert_array_equal(pi, i)

def test_fixed_grid():
    si = IsingSpinIce(size=(4,4))
    L = si.L

    assert si.lattice_spacing == 1

    #
    # 4x4 grid fits perfectly
    #
    grid = si.fixed_grid((4, 4))
    assert grid.cell_size == (1, 1)
    assert grid.size == (4, 4)

    assert grid.grid_index(L[0,0]) == (0,0)
    spin_indices = si.all_indices()
    grid_indices = grid.grid_index(spin_indices)
    assert_array_equal(grid_indices, np.transpose(si.labels))

    #
    # 2x2 grid evenly divides lattice spacing
    #
    grid = si.fixed_grid((2,2))
    assert grid.cell_size == (2, 2)
    assert grid.size == (2, 2)

    # cell (0,0)
    i = [L[0,0], L[0,1], L[1,0], L[1,1]]
    gi = grid.grid_index(i)
    assert np.all(np.transpose(gi) == [0,0])
    assert_array_equal(grid.point_index((0,0)), i)

    # cell (0,1)
    i = [L[0,2], L[0,3], L[1,2], L[1,3]]
    gi = grid.grid_index(i)
    assert np.all(np.transpose(gi) == [0,1])
    assert_array_equal(grid.point_index((0,1)), i)

    # cell (1,0)
    i = [L[2,0], L[2,1], L[3,0], L[3,1]]
    gi = grid.grid_index(i)
    assert np.all(np.transpose(gi) == [1,0])
    assert_array_equal(grid.point_index((1,0)), i)

    # cell (1,1)
    i = [L[2,2], L[2,3], L[3,2], L[3,3]]
    gi = grid.grid_index(i)
    assert np.all(np.transpose(gi) == [1,1])
    assert_array_equal(grid.point_index((1,1)), i)


    #
    # 3x2 grid does not evently divide lattice_spacing
    #
    grid = si.fixed_grid((3,2))
    assert grid.cell_size == (4/3, 2)
    assert grid.size == (2, 3)

    # cell (0,0)
    i = [L[0,0], L[1,0]]
    pi = grid.point_index((0,0))
    assert_array_equal(pi, i)

    # cell (0,1)
    i = [L[0,1], L[0,2], L[1,1], L[1,2]]
    pi = grid.point_index((0,1))
    assert_array_equal(pi, i)

    # cell (0,2)
    i = [L[0,3], L[1,3]]
    pi = grid.point_index((0,2))
    assert_array_equal(pi, i)

    # cell (1,0)
    i = [L[2,0], L[3,0]]
    pi = grid.point_index((1,0))
    assert_array_equal(pi, i)

    # cell (1,1)
    i = [L[2,1], L[2,2], L[3,1], L[3,2]]
    pi = grid.point_index((1,1))
    assert_array_equal(pi, i)

    # cell (1,2)
    i = [L[2,3], L[3,3]]
    pi = grid.point_index((1,2))
    assert_array_equal(pi, i)

def test_data_order():
    # Test that internal arrays are always in C order. The user might pass in
    # arrays in F order, which will cause problems with opencl which very much
    # assumes C order.
    #
    # Data order only applies to arrays with ndim > 1.  Currently the only such
    # array that is allowed to be modified by the user is h_ext.

    h_ext = np.random.uniform(size=(2, 4*4))
    h_ext = h_ext.T
    assert np.isfortran(h_ext)

    si = IsingSpinIce(size=(4,4), h_ext=h_ext)
    assert not np.isfortran(si.h_ext)

    si = IsingSpinIce(size=(4,8))
    assert not np.isfortran(si.h_ext)
    h_ext = np.random.uniform(size=(2, 4*8)).T
    assert np.isfortran(h_ext)
    si.set_h_ext(h_ext)
    assert not np.isfortran(si.h_ext)

def test_set_angle(opencl):
    params = dict(
        size=(10,10),
        neighbor_distance=3
    )
    params.update(opencl)

    model = IsingSpinIce(**params)

    # Create a CustomSpinIce with expected result
    angle = np.random.uniform(0, 360, model.spin_count)
    angle = np.deg2rad(angle)
    custom = CustomSpinIce(magnet_coords=model.pos, magnet_angles=angle, radians=True, **params)

    assert_array_equal(model.pos, custom.pos)
    assert not np.all(model.angle == custom.angle)
    assert not np.all(model.m == custom.m)
    assert not np.all(model.dipolar_fields() == custom.dipolar_fields())

    # Change angles of model
    model.set_angle(angle)

    assert_array_equal(model.pos, custom.pos)
    assert_array_equal(model.angle, custom.angle)
    assert_array_equal(model.m, custom.m)
    assert_array_equal(model.dipolar_fields(), custom.dipolar_fields())

def test_set_angle_spin_axis(opencl):
    params = dict(
        size=(10,10),
        neighbor_distance=3,
        spin_axis=90,
    )
    params.update(opencl)

    model = IsingSpinIce(**params)

    # Create a CustomSpinIce with expected result
    angle = np.linspace(-360, 360, model.spin_count)
    custom = CustomSpinIce(magnet_coords=model.pos, magnet_angles=angle, radians=False, **params)

    expect = angle % 360
    expect[expect>180] -= 180
    expect = np.radians(expect)

    assert_allclose(custom.angle, expect)

    assert_array_equal(model.pos, custom.pos)
    assert not np.all(model.angle == custom.angle)
    assert not np.all(model.m == custom.m)
    assert not np.all(model.dipolar_fields() == custom.dipolar_fields())

    # Change angles of model
    model.set_angle(np.radians(angle))

    assert_array_equal(model.pos, custom.pos)
    assert_array_equal(model.angle, custom.angle)
    assert_array_equal(model.m, custom.m)
    assert_array_equal(model.dipolar_fields(), custom.dipolar_fields())

def test_set_pos(opencl):
    params = dict(
        size=(10,10),
        neighbor_distance=3
    )
    params.update(opencl)

    model = IsingSpinIce(**params)

    # Create a CustomSpinIce with expected result
    pos = model.pos + .3*np.random.uniform(-1, 1, model.pos.shape)
    custom = CustomSpinIce(magnet_coords=pos, magnet_angles=model.angle, radians=True, **params)

    assert not np.all(model.pos == custom.pos)
    assert_array_equal(model.angle, custom.angle)
    assert_array_equal(model.m, custom.m)
    assert not np.all(model.dipolar_fields() == custom.dipolar_fields())

    # Change positions of model
    model.set_pos(pos)

    assert_array_equal(model.pos, custom.pos)
    assert_array_equal(model.angle, custom.angle)
    assert_array_equal(model.m, custom.m)
    assert_array_equal(model.dipolar_fields(), custom.dipolar_fields())

def test_set_geometry(opencl):
    params = dict(
        size=(10,10),
        neighbor_distance=3
    )
    params.update(opencl)

    model = IsingSpinIce(**params)

    # Create a CustomSpinIce with expected result
    pos = model.pos + .3*np.random.uniform(-1, 1, model.pos.shape)
    angle = np.random.uniform(0, 360, model.spin_count)
    angle = np.deg2rad(angle)
    custom = CustomSpinIce(magnet_coords=pos, magnet_angles=angle, radians=True, **params)

    assert not np.all(model.pos == custom.pos)
    assert not np.all(model.angle == custom.angle)
    assert not np.all(model.m == custom.m)
    assert not np.all(model.dipolar_fields() == custom.dipolar_fields())

    # Change positions and angles of model
    model.set_geometry(pos, angle)

    assert_array_equal(model.pos, custom.pos)
    assert_array_equal(model.angle, custom.angle)
    assert_array_equal(model.m, custom.m)
    assert_array_equal(model.dipolar_fields(), custom.dipolar_fields())

#                                              NN,        NNN, 3NN,        4NN,          5NN
@pytest.mark.parametrize("neighbor_distance", [ 0.1, 1, np.sqrt(2),   2, np.sqrt(5), 2*np.sqrt(2)])
def test_set_neighbor_distance(opencl, neighbor_distance):
    # nearest neighbors (default)
    params = dict(size=(10, 10))
    params.update(opencl)
    si = IsingSpinIce(**params)

    for i in np.arange(0.1, 10):
        si.dipolar_fields()
        si.set_neighbor_distance(i)

    expect = IsingSpinIce(neighbor_distance=neighbor_distance, **params)
    si.set_neighbor_distance(neighbor_distance)
    si.total_fields()

    assert si.neighbor_distance == expect.neighbor_distance
    assert si.num_neighbors == expect.num_neighbors
    assert_array_equal(si._neighbor_list, expect._neighbor_list)
    assert_array_equal(si.dipolar_fields(), expect.dipolar_fields())

def test_zero_neighbors(opencl):
    si = IsingSpinIce(neighbor_distance=0, **opencl)
    assert si.num_neighbors == 0
    assert all([len(si.neighbors(i)) == 0 for i in si.indices()])
    assert_array_equal(si.total_fields(), np.zeros((si.spin_count, 2)))
    assert_array_equal(si.dipolar_fields(), np.zeros((si.spin_count, 2)))

    si.set_neighbor_distance(0.1)
    assert si.num_neighbors == 0
    assert all([len(si.neighbors(i)) == 0 for i in si.indices()])
    assert_array_equal(si.total_fields(), np.zeros((si.spin_count, 2)))
    assert_array_equal(si.dipolar_fields(), np.zeros((si.spin_count, 2)))

    si.set_neighbor_distance(1)
    assert si.num_neighbors > 0
    assert all([len(si.neighbors(i)) > 0 for i in si.indices()])
    h_tot = si.total_fields()
    assert all(norm(h_tot, axis=0) > 0)
    h_dip = si.dipolar_fields()
    assert all(norm(h_dip, axis=0) > 0)

def test_set_sw_params(opencl):
    si = IsingSpinIce(size=(1, 1), hc=1, spin_angle=0, **opencl)

    bs = [.4, 1]
    cs = [.5, 1]
    betas = [1, 2, 3, 4]
    gammas = [1, 2, 3, 4]

    for b, c, beta, gamma in itertools.product(bs, cs, betas, gammas):
        si.set_sw_params(b, c, beta, gamma)
        # si.sw_params = b, c, beta, gamma
        assert si.sw_params == (b, c, beta, gamma)
        hc = si.hc

        # Test that switching threshold is correct
        inside = gsw_astroid(b, c, beta, gamma, hc*0.99, rotation=0,
                             resolution=10, angle_range=(np.pi/2, 3*np.pi/2))

        outside = gsw_astroid(b, c, beta, gamma, hc*1.01, rotation=0,
                              resolution=10, angle_range=(np.pi/2, 3*np.pi/2))

        for h_ext in inside[1:-1]:
            si.set_h_ext(h_ext)
            assert len(si.flippable()) == 0

        for h_ext in outside[1:-1]:
            si.set_h_ext(h_ext)
            assert len(si.flippable()) == 1

        # Test that astroid tree is correct
        intersection = gsw_astroid(b, c, beta, gamma, hc, rotation=0,
                                   resolution=10, angle_range=(np.pi/2, np.pi))

        for h_ext in intersection[1:-2]:
            # Look up nearest point on astroid
            astroid_points = si.astroid_tree.data
            distances, indices = si.astroid_tree.query(h_ext, k=1)
            nearest = astroid_points[indices]
            assert_allclose(nearest, h_ext, atol=1e-2)

def test_astroid_params():
    si = IsingSpinIce(size=(1, 1), astroid_params="stadium220x80x20")
    params = astroid_params(shape='stadium', width=220, height=80, thickness=20)

    b, c, beta, gamma = si.sw_params
    assert si.hc == params['hc']
    assert b == params['sw_b']
    assert c == params['sw_c']
    assert beta == params['sw_beta']
    assert gamma == params['sw_gamma']

# Reading params from tablefile
@pytest.fixture
def dataset(tmpdir_factory):
    basedir = tmpdir_factory.mktemp('test')
    index = pd.DataFrame({'A': np.arange(0,1,0.1), 'B': np.arange(0,10)//2, 'C': list('abcdefghij')})
    params = {'foo': 1, 'bar': [1,2,3]}
    info = {'array': np.array([3,2,1])}
    ds = Dataset(index, params, info, basedir)
    ds.save()
    return ds

def test_hc_from_file(dataset, tmpdir, opencl):
    # make hc.csv and .npz/hc for testing
    si1 = IsingSpinIce(disorder=0.05, use_opencl=opencl)
    hc_file = path.join(tmpdir, 'test_hc.csv')
    save_table(si1.threshold, hc_file)

    hc_archive_file = path.join(dataset.basepath + 'test.npz', 'hc')
    save_table(pd.DataFrame({'threshold': si1.threshold}), hc_archive_file)

    # init hc from csv file
    si2 = IsingSpinIce(use_opencl=opencl, hc=hc_file)
    assert_allclose(si1.threshold, si2.hc)
    assert_allclose(si1.threshold, si2.threshold)

    # init hc from dataset hc file
    si2 = IsingSpinIce(use_opencl=opencl, hc=hc_archive_file)
    assert_allclose(si1.threshold, si2.hc)
    assert_allclose(si1.threshold, si2.threshold)

    # set hc from csv file
    si2 = IsingSpinIce(use_opencl=opencl, disorder=0.05)
    disorder_factor = si2.threshold / si2.hc
    si2.set_hc_from_tablefile(hc_file)
    assert_allclose(si2.hc, si1.threshold)
    assert_allclose(si2.threshold, si1.threshold * disorder_factor)

    # set hc from dataset hc file
    si2 = IsingSpinIce(use_opencl=opencl, disorder=0.05)
    disorder_factor = si2.threshold / si2.hc
    si2.set_hc_from_tablefile(hc_archive_file)
    assert_allclose(si2.hc, si1.threshold)
    assert_allclose(si2.threshold, si1.threshold * disorder_factor)

def test_spin_from_file(dataset, tmpdir, opencl):
    # make init.csv and .npz/init .npz/spin for testing
    si1 = IsingSpinIce(use_opencl=opencl, init="random")
    init_file = path.join(tmpdir, 'iNiT.csv')
    save_table(si1.spin, init_file)

    # mimic the saving of the init and spin files in runner
    init_archive_file = path.join(dataset.basepath + 'test.npz', 'init')
    cols = label_columns(si1.labels, prefix='init')
    save_table(pd.DataFrame([si1.spin.copy()], columns=cols), init_archive_file)

    # make spin time series
    spin = []
    for _ in range(3):
        spin.append(si1.spin.copy())
        si1.randomize()
    spin_archive_file = path.join(dataset.basepath + 'test.npz', 'spin')
    cols = label_columns(si1.labels, prefix='spin')
    spin_df = pd.DataFrame(spin, columns=cols, index=[0, 10, 20], dtype=spin[0].dtype)
    spin_df.index.name = 't'
    save_table(spin_df, spin_archive_file)

    # init spin from csv file
    si2 = IsingSpinIce(use_opencl=opencl, init=init_file)
    assert_array_equal(si2.spin, spin[0])

    # init spin from dataset init file
    si2 = IsingSpinIce(use_opencl=opencl, init=init_archive_file)
    assert_array_equal(si2.spin, spin[0])

    # init spin from dataset spin file, filter on t
    si2 = IsingSpinIce(use_opencl=opencl, init=spin_archive_file+"[10]")
    assert_array_equal(si2.spin, spin[1])

    # set spin from csv file
    si2 = IsingSpinIce(use_opencl=opencl, init="random")
    si2.set_spin_from_tablefile(init_file)
    assert_array_equal(si2.spin, spin[0])

    # set spin from dataset init file
    si2 = IsingSpinIce(use_opencl=opencl, init="random")
    si2.set_spin_from_tablefile(init_archive_file)
    assert_array_equal(si2.spin, spin[0])

    # set spin from dataset spin file, filter on t
    si2 = IsingSpinIce(use_opencl=opencl, init="random")
    si2.set_spin_from_tablefile(spin_archive_file, 10)
    assert_array_equal(si2.spin, spin[1])
