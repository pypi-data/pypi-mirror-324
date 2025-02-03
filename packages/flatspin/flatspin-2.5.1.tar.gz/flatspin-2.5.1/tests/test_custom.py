import numpy as np
from numpy.testing import assert_array_equal
from .utils import approx, assert_allclose
import pytest

from flatspin import CustomSpinIce

def test_spin_axis_auto():
    angle = [-90., 90.]
    pos = np.column_stack((np.arange(len(angle)), np.zeros(len(angle))))
    si = CustomSpinIce(magnet_coords=pos, magnet_angles=angle)

    assert_array_equal(si.pos, pos)
    assert_array_equal(np.degrees(si.angle), angle)

    # spin axis down, flip the 90 degree spin
    expect = [-90., -90.]
    si = CustomSpinIce(magnet_coords=pos, magnet_angles=angle, spin_axis="auto")
    assert si._spin_axis == approx(-90)
    assert_allclose(np.degrees(si.angle), expect)

    # spin axis down, flip the 85 degree spin
    angle = [-85., 85.]
    expect = [-85., -95.]
    si = CustomSpinIce(magnet_coords=pos, magnet_angles=angle, spin_axis="auto")
    assert si._spin_axis == approx(-90)
    assert_allclose(np.degrees(si.angle), expect)

    # spin axis down to the right [-2, 1]
    angle = [-90, 90, 0]
    expect = [-90, -90, 0]
    pos = np.column_stack((np.arange(len(angle)), np.zeros(len(angle))))
    si = CustomSpinIce(magnet_coords=pos, magnet_angles=angle, spin_axis="auto")
    assert si._spin_axis == approx(np.degrees(np.arctan2(-2, 1)))
    assert_allclose(np.degrees(si.angle), expect)

    # spin axis at -45 degree
    angle = [-90, 90, 0, 180]
    expect = [-90, -90, 0, 0]
    pos = np.column_stack((np.arange(len(angle)), np.zeros(len(angle))))
    si = CustomSpinIce(magnet_coords=pos, magnet_angles=angle, spin_axis="auto")
    assert si._spin_axis == approx(-45)
    assert_allclose(np.degrees(si.angle), expect)

@pytest.mark.parametrize("h_ext", [(0,0), (1,1), (-1,1), (1,-1), (-1,-1)])
@pytest.mark.parametrize("spin_axis", np.linspace(0, 360, 5))
def test_to_global_frame(h_ext, spin_axis):
    angles = np.linspace(-360, 360, 9)
    pos = np.column_stack((np.arange(len(angles)), np.zeros(len(angles))))

    si = CustomSpinIce(magnet_coords=pos, magnet_angles=angles, spin_axis=spin_axis)
    si.randomize()
    si.set_h_ext(h_ext)

    external_fields = si.external_fields()
    external_fields_global_frame = si.to_global_frame(external_fields)

    assert_allclose(external_fields_global_frame, si.h_ext)

@pytest.mark.parametrize("h_ext", [(0,0), (1,1), (-1,1), (1,-1), (-1,-1)])
@pytest.mark.parametrize("spin_axis", np.linspace(0, 360, 5))
def test_to_mag_frame(h_ext, spin_axis):
    angles = np.linspace(-360, 360, 9)
    pos = np.column_stack((np.arange(len(angles)), np.zeros(len(angles))))

    si = CustomSpinIce(magnet_coords=pos, magnet_angles=angles, spin_axis=spin_axis)
    si.randomize()
    si.set_h_ext(h_ext)

    external_fields = si.external_fields()
    h_ext_magnet_frame = si.to_mag_frame(si.h_ext)

    assert_allclose(external_fields, h_ext_magnet_frame)
