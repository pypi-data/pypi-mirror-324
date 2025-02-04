import unittest
from typing import Any, Callable, Iterable, Mapping

import numpy as np


class NpyTestCase(unittest.TestCase):
    def assertArrayEqual(
        self, a1: np.ndarray, a2: np.ndarray, *, equal_nan: bool = False
    ) -> None:
        are_equal = np.array_equal(a1, a2, equal_nan=equal_nan)
        if not are_equal:
            raise self.failureException("The given arrays are not equal.")

    def assertArrayNotEqual(
        self, a1: np.ndarray, a2: np.ndarray, *, equal_nan: bool = False
    ) -> None:
        are_equal = np.array_equal(a1, a2, equal_nan=equal_nan)
        if are_equal:
            raise self.failureException("The given arrays are equal.")

    def assertAllclose(
        self, a: np.ndarray, b: np.ndarray, *, rtol=1.0e-5, atol=1.0e-8, equal_nan=False
    ) -> None:
        are_close = np.allclose(a=a, b=b, rtol=rtol, atol=atol, equal_nan=equal_nan)
        if not are_close:
            raise self.failureException("The given arrays are not close.")

    def assertNotAllclose(
        self, a: np.ndarray, b: np.ndarray, *, rtol=1.0e-5, atol=1.0e-8, equal_nan=False
    ) -> None:
        are_close = np.allclose(a=a, b=b, rtol=rtol, atol=atol, equal_nan=equal_nan)
        if are_close:
            raise self.failureException("The given arrays are close.")

    def assertIssubdtype(self, dtype: Any, super_dtype: Any, /) -> None:
        is_subdtype = np.issubdtype(dtype, super_dtype)

        if isinstance(dtype, np.ndarray):
            raise ValueError(
                f'This function expects a dtype for argument "dtype" instead of an array.'
            )
        if isinstance(super_dtype, np.ndarray):
            raise ValueError(
                f'This function expects a dtype for argument "super_dtype" instead of an array.'
            )

        if not is_subdtype:
            raise self.failureException(
                f"The dtype {dtype} is not a subdtype of {super_dtype}."
            )

    def assertAll(self, array: np.ndarray) -> None:
        if not np.all(array):
            raise self.failureException("Not all elements of the array are true.")

    def assertAny(self, array: np.ndarray) -> None:
        if not np.any(array):
            raise self.failureException("All elements of the array are false.")
