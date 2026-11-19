"""R4R1 focused regression for independent fourth-order sign erratum."""
from pathlib import Path
import sys

import pytest

HERE = Path(__file__).resolve().parent

sys.path.insert(
    0,
    str(HERE)
)

from verify_gamma1_00r4r1 import (
    calculate_signs,
    sha,
    PROFILE_REL,
    PROFILE_SHA,
    ROOT,
)


@pytest.fixture(scope='module')
def observed():
    return calculate_signs(
        ROOT/PROFILE_REL
    )


def test_original_native_profile_exact_hash():
    assert sha(ROOT/PROFILE_REL) == PROFILE_SHA


def test_independent_second_order_full_sign_counts(observed):
    assert (
        observed['second_full_outward'],
        observed['second_full_inward']
    ) == (248, 40)


def test_inner_negative_control_is_mixed(observed):
    assert (
        observed['second_inner_samples'],
        observed['second_inner_outward'],
        observed['second_inner_inward']
    ) == (56, 16, 40)


def test_outer_second_order_control(observed):
    assert (
        observed['second_outer_samples'],
        observed['second_outer_outward'],
        observed['second_outer_inward']
    ) == (232, 232, 0)


def test_fourth_order_corrected_sign_counts(observed):
    assert (
        observed['fourth_tail_samples'],
        observed['fourth_tail_outward'],
        observed['fourth_tail_inward']
    ) == (128, 128, 0)


def test_fourth_order_positive_bounded_values(observed):
    assert (
        0
        < observed['fourth_tail_min']
        < observed['fourth_tail_max']
    )

    assert (
        3.8e-8
        < observed['fourth_tail_min']
        < 3.9e-8
    )


def test_old_verifier_exact_double_negation(observed):
    assert (
        observed['original_verifier_wrong_sign_outward'],
        observed['original_verifier_wrong_sign_inward']
    ) == (0, 128)

    assert observed[
        'original_verifier_old_minus_corrected_max_abs'
    ] == 0.


def test_outer_box_still_contains_source(observed):
    assert observed['outer_box_cells'] == 46

    assert observed[
        'outer_box_max_F_amplitude'
    ] > 0
