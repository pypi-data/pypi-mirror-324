from __future__ import annotations
import numpy
import ostk.core.type
import ostk.mathematics.curve_fitting
import typing
__all__ = ['BarycentricRational', 'CubicSpline', 'Linear']
class BarycentricRational(ostk.mathematics.curve_fitting.Interpolator):
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __init__(self, x: numpy.ndarray[numpy.float64[m, 1]], y: numpy.ndarray[numpy.float64[m, 1]]) -> None:
        ...
    @typing.overload
    def evaluate(self, x: numpy.ndarray[numpy.float64[m, 1]]) -> numpy.ndarray[numpy.float64[m, 1]]:
        ...
    @typing.overload
    def evaluate(self, x: float) -> float:
        ...
class CubicSpline(ostk.mathematics.curve_fitting.Interpolator):
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    @typing.overload
    def __init__(self, x: numpy.ndarray[numpy.float64[m, 1]], y: numpy.ndarray[numpy.float64[m, 1]]) -> None:
        ...
    @typing.overload
    def __init__(self, y: numpy.ndarray[numpy.float64[m, 1]], x_0: ostk.core.type.Real, h: ostk.core.type.Real) -> None:
        ...
    @typing.overload
    def evaluate(self, x: numpy.ndarray[numpy.float64[m, 1]]) -> numpy.ndarray[numpy.float64[m, 1]]:
        ...
    @typing.overload
    def evaluate(self, x: float) -> float:
        ...
class Linear(ostk.mathematics.curve_fitting.Interpolator):
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __init__(self, x: numpy.ndarray[numpy.float64[m, 1]], y: numpy.ndarray[numpy.float64[m, 1]]) -> None:
        ...
    @typing.overload
    def evaluate(self, x: numpy.ndarray[numpy.float64[m, 1]]) -> numpy.ndarray[numpy.float64[m, 1]]:
        ...
    @typing.overload
    def evaluate(self, x: float) -> float:
        ...
