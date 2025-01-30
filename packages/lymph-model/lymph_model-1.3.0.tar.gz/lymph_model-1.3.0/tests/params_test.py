"""Test if setting params via the named subset works correctly."""

import pytest

from lymph import models

from .fixtures import (
    RNG,
    _create_random_frozen_dist,
    _create_random_parametric_dist,
    get_graph,
)


@pytest.fixture()
def binary_unilateral_model() -> models.Unilateral:
    """Return a binary unilateral model."""
    model = models.Unilateral(graph_dict=get_graph(size="small"))
    model.set_distribution(
        t_stage="early",
        distribution=_create_random_frozen_dist(max_time=model.max_time),
    )
    model.set_distribution(
        t_stage="late",
        distribution=_create_random_parametric_dist(max_time=model.max_time),
    )
    return model


@pytest.fixture()
def binary_bilateral_model() -> models.Bilateral:
    """Return a binary bilateral model."""
    model = models.Bilateral(graph_dict=get_graph(size="small"))
    model.set_distribution(
        t_stage="early",
        distribution=_create_random_frozen_dist(max_time=model.max_time),
    )
    model.set_distribution(
        t_stage="late",
        distribution=_create_random_parametric_dist(max_time=model.max_time),
    )
    return model


def test_set_named_params_default_behavior(
    binary_unilateral_model: models.Unilateral,
) -> None:
    """Ensure `set_named_params` works as `set_params` when no `named_params` set."""
    params = binary_unilateral_model.get_params(as_dict=True)
    new_params = {param: RNG.uniform() for param in params.keys()}
    binary_unilateral_model.set_named_params(**new_params)
    assert new_params == binary_unilateral_model.get_params(as_dict=True)


def test_named_params_setter(
    binary_unilateral_model: models.Unilateral,
    binary_bilateral_model: models.Midline,
) -> None:
    """Check that setting `named_params` works correctly."""
    with pytest.raises(ValueError):
        binary_unilateral_model.named_params = ["some_param"]

    with pytest.raises(ValueError):
        binary_unilateral_model.named_params = ["invalid identifier!"]

    with pytest.raises(ValueError):
        binary_unilateral_model.named_params = 123

    with pytest.raises(ValueError):
        binary_bilateral_model.named_params = ["spread_ipsi"]

    params = binary_unilateral_model.get_params(as_dict=True).keys()
    params_subset = [param for param in params if RNG.uniform() > 0.5]
    binary_unilateral_model.named_params = params_subset

    for stored, subset in zip(
        binary_unilateral_model.named_params,
        params_subset,
        strict=True,
    ):
        assert stored == subset

    binary_bilateral_model.named_params = ["ipsi_spread"]
    assert binary_bilateral_model.named_params == ["ipsi_spread"]


def test_set_named_params_named_easy_subset(
    binary_unilateral_model: models.Unilateral,
) -> None:
    """Ensure `set_named_params` works correctly with an easy subset.

    An "easy subset" is a literal subset of the params.
    """
    params = binary_unilateral_model.get_params(as_dict=True)
    new_params = {param: RNG.uniform() for param in params.keys()}
    params_subset = {k: RNG.uniform() for k in params if RNG.uniform() > 0.5}

    binary_unilateral_model.set_params(**new_params)
    binary_unilateral_model.named_params = params_subset.keys()
    binary_unilateral_model.set_named_params(**params_subset)

    for param, new_val in new_params.items():
        stored_params = binary_unilateral_model.get_params(as_dict=True)
        if param in params_subset:
            assert params_subset[param] == stored_params[param]
        else:
            assert new_val == stored_params[param]

    assert set(params_subset.keys()) == set(binary_unilateral_model.named_params)


def test_set_named_params_raises(
    binary_unilateral_model: models.Unilateral,
) -> None:
    """Ensure `set_named_params` raises when provided with invalid keys."""
    binary_unilateral_model.named_params = ["spread"]
    with pytest.raises(ValueError):
        binary_unilateral_model.set_named_params(invalid=RNG.uniform())


def test_set_named_params_named_hard_subset(
    binary_unilateral_model: models.Unilateral,
) -> None:
    """Ensure `set_named_params` works correctly with a hard subset.

    A "hard subset" is a subset that includes "global params". I.e., `spread` would
    not be a literal subset, because those are nemad something like `TtoII_spread`. But
    the `set_params()` method does accept it and will set all spread params with the
    provided value. It should be possible to set the `named_params` to such names and
    then set them with the `set_named_params()` method.
    """
    params = binary_unilateral_model.get_params(as_dict=True)
    new_params = {param: RNG.uniform() for param in params.keys()}
    first_lnl = list(binary_unilateral_model.graph.lnls.keys())[0]
    first_lnl_param = f"Tto{first_lnl}_spread"
    params_subset = {k: RNG.uniform() for k in ["spread", first_lnl_param]}

    binary_unilateral_model.set_params(**new_params)
    binary_unilateral_model.named_params = params_subset.keys()
    binary_unilateral_model.set_named_params(**params_subset)

    stored_params = binary_unilateral_model.get_params(as_dict=True)
    for param, new_val, stored_param in zip(
        params.keys(),
        new_params.values(),
        stored_params.values(),
        strict=True,
    ):
        if param == first_lnl_param:
            assert params_subset[first_lnl_param] == stored_param
        elif "spread" in param:
            assert params_subset["spread"] == stored_param
        else:
            assert new_val == stored_param


def test_set_global_params_for_side(
    binary_bilateral_model: models.Bilateral,
) -> None:
    """Check that setting e.g. `"ipsi_spread"` works as global param to ipsi side."""
    params = binary_bilateral_model.get_params(as_dict=True)
    new_params = {param: RNG.uniform() for param in params.keys()}

    binary_bilateral_model.named_params = ["ipsi_spread"]
    binary_bilateral_model.set_params(**new_params)
    ipsi_spread_val = RNG.uniform()
    binary_bilateral_model.set_named_params(ipsi_spread=ipsi_spread_val)

    ipsi_stored_params = binary_bilateral_model.ipsi.get_params(as_dict=True)

    for param, stored_param in ipsi_stored_params.items():
        if "spread" in param:
            assert stored_param == ipsi_spread_val
        else:
            assert stored_param in new_params.values()
