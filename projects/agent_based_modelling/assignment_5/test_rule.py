import numpy as np
import pytest
from numpy.testing import assert_array_equal

from projects.agent_based_modelling.assignment_5.rule import CUSTOM_STEP_FUNCTIONS, Rule

BITS = 3


@pytest.fixture(name="rule", params=CUSTOM_STEP_FUNCTIONS)
def fixture_rule(request):
    return Rule(number=request.param)


@pytest.mark.parametrize(
    "arr",
    [np.array([int(bit) for bit in f"{number:0{BITS}b}"]) for number in range(2**BITS)],
    ids=[f"{number:0{BITS}b}" for number in range(2**BITS)],
)
def test_rules(arr, rule):
    assert rule.step_function is not rule.generic_step_function
    assert_array_equal(rule.step_function(arr), rule.generic_step_function(arr))
