"""Type aliases and protocols used in the lymph package."""

from abc import ABC, abstractmethod
from collections.abc import Iterable
from typing import Literal, Protocol, TypeVar

import numpy as np
import pandas as pd


class DataWarning(UserWarning):
    """Warnings related to potential data issues."""


class HasSetParams(Protocol):
    """Protocol for classes that have a ``set_params`` method."""

    def set_params(self, *args: float, **kwargs: float) -> tuple[float]:
        """Set the parameters of the class."""
        ...


class HasGetParams(Protocol):
    """Protocol for classes that have a ``get_params`` method."""

    def get_params(
        self,
        as_dict: bool = True,
        as_flat: bool = True,
    ) -> tuple[float] | dict[str, float]:
        """Return the parameters of the class."""
        ...


GraphDictType = dict[tuple[str, str], list[str]]
"""Type alias for a graph dictionary.

A dictionary of this form specifies the structure of the underlying graph. Example:

>>> graph_dict = {
...     ("tumor", "T"): ["I", "II", "III"],
...     ("lnl", "I"): ["II"],
...     ("lnl", "II"): ["III"],
...     ("lnl", "III"): [],
... }
"""

ParamsType = Iterable[float] | dict[str, float]
"""Type alias for how parameters are passed around.

This is e.g. the type that the :py:meth:`.Model.get_params` method returns.
"""

InvolvementIndicator = Literal[
    False,
    0,
    "healthy",
    True,
    1,
    "involved",
    "micro",
    "macro",
    "notmacro",
]
"""Type alias for how to encode lymphatic involvement for a single lymph node level.

The choices ``"micro"``, ``"macro"``, and ``"notmacro"`` are only relevant for the
trinary models.
"""

PatternType = dict[str, InvolvementIndicator | None]
"""Type alias for an involvement pattern.

An involvement pattern is a dictionary with keys for the lymph node levels and values
for the involvement of the respective lymph nodes. The values are either True, False,
or None, which means that the involvement is unknown.

TODO: Document the new possibilities to specify trinary involvment.
See :py:func:`.matrix.compute_encoding`

>>> pattern = {"I": True, "II": False, "III": None}
"""

DiagnosisType = dict[str, PatternType]
"""Type alias for a diagnosis, which is an involvement pattern per diagnostic modality.

>>> diagnosis = {
...     "CT": {"I": True, "II": False, "III": None},
...     "MRI": {"I": True, "II": True, "III": None},
... }
"""


ModelT = TypeVar("ModelT", bound="Model")


class Model(ABC):
    """Abstract base class for models.

    This class provides a scaffold for the methods that any model for lymphatic
    tumor progression should implement.
    """

    @abstractmethod
    def get_params(
        self: ModelT,
        as_dict: bool = True,
        as_flat: bool = True,
    ) -> ParamsType:
        """Return the parameters of the model.

        The parameters are returned as a dictionary if ``as_dict`` is True, and as
        an iterable of floats otherwise. The argument ``as_flat`` determines whether
        the returned dict is flat or nested. This is helpful, because a model may call
        the ``get_params`` method of other instances, which can be fused to get a
        flat dictionary.
        """
        raise NotImplementedError

    def get_num_dims(self: ModelT, mode: Literal["HMM", "BN"] = "HMM") -> int:
        """Return the number of dimensions of the parameter space.

        A hidden Markov model (``mode="HMM"``) typically has more parameters than a
        Bayesian network (``mode="BN"``), because it we need parameters for the
        distributions over diagnosis times. Your can read more about that in the
        :py:mod:`lymph.diagnosis_times` module.
        """
        # pylint: disable=no-member
        num = len(self.get_params())
        if mode == "BN":
            num -= len(self.get_distribution_params())
        return num

    @abstractmethod
    def set_params(self: ModelT, *args: float, **kwargs: float) -> tuple[float]:
        """Set the parameters of the model.

        The parameters may be passed as positional or keyword arguments. The positional
        arguments are used up one by one by the ``set_params`` methods the model calls.
        Keyword arguments override the positional arguments.
        """
        raise NotImplementedError

    @abstractmethod
    def state_dist(
        self: ModelT,
        t_stage: str,
        mode: Literal["HMM", "BN"] = "HMM",
    ) -> np.ndarray:
        """Return the prior state distribution of the model.

        The state distribution is the probability of the model being in any of the
        possible hidden states.
        """
        raise NotImplementedError

    def obs_dist(
        self: ModelT,
        given_state_dist: np.ndarray | None = None,
        t_stage: str = "early",
        mode: Literal["HMM", "BN"] = "HMM",
    ) -> np.ndarray:
        """Return the distribution over observational states.

        If ``given_state_dist`` is ``None``, it will first compute the
        :py:meth:`.state_dist` using the arguments ``t_stage`` and ``mode`` (which are
        otherwise ignored). Then it multiplies the distribution over (hidden) states
        with the specificity and sensitivity values stored in the model (see
        :py:meth:`.modalities.Composite`) and marginalizes over the hidden states.
        """
        raise NotImplementedError

    @abstractmethod
    def load_patient_data(
        self: ModelT,
        patient_data: pd.DataFrame,
    ) -> None:
        """Load patient data in `LyProX`_ format into the model.

        .. _LyProX: https://lyprox.org/
        """
        raise NotImplementedError

    @abstractmethod
    def likelihood(
        self: ModelT,
        given_params: ParamsType | None = None,
        log: bool = True,
    ) -> float:
        """Return the likelihood of the model given the parameters.

        The likelihood is returned in log space if ``log`` is True, and in linear space
        otherwise. The parameters may be passed as positional or keyword arguments.
        They are then passed to the :py:meth:`set_params` method first.
        """
        raise NotImplementedError

    @abstractmethod
    def posterior_state_dist(
        self: ModelT,
        given_params: ParamsType | None = None,
        given_state_dist: np.ndarray | None = None,
        given_diagnosis: dict[str, PatternType] | None = None,
    ) -> np.ndarray:
        """Return the posterior state distribution using the ``given_diagnosis``.

        The posterior state distribution is the probability of the model being in a
        certain state given the diagnosis. The ``given_params`` are passed to the
        :py:meth:`set_params` method. Alternatively to parameters, one may also pass
        a ``given_state_dist``, which is effectively the precomputed prior from calling
        :py:meth:`.state_dist`.
        """
        raise NotImplementedError

    def marginalize(
        self,
        involvement: dict[str, PatternType] | None = None,
        given_state_dist: np.ndarray | None = None,
        t_stage: str = "early",
        mode: Literal["HMM", "BN"] = "HMM",
    ) -> float:
        """Marginalize ``given_state_dist`` over matching ``involvement`` patterns.

        Any state that matches the provided ``involvement`` pattern is marginalized
        over. For this, the :py:func:`.matrix.compute_encoding` function is used.

        If ``given_state_dist`` is ``None``, it will be computed by calling
        :py:meth:`.state_dist` with the given ``t_stage`` and ``mode``. These arguments
        are ignored if ``given_state_dist`` is provided.
        """
        raise NotImplementedError

    @abstractmethod
    def risk(
        self,
        involvement: PatternType | None = None,
        given_params: ParamsType | None = None,
        given_state_dist: np.ndarray | None = None,
        given_diagnosis: dict[str, PatternType] | None = None,
    ) -> float:
        """Return the risk of ``involvement``, given params/state_dist and diagnosis."""
        raise NotImplementedError
