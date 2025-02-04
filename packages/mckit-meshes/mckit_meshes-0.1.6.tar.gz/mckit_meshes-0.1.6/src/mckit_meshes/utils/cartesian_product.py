"""Apply function to cartesian product of arrays."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from itertools import product

import numpy as np

if TYPE_CHECKING:
    from collections.abc import Callable
    from numpy.typing import NDArray


def cartesian_product(
    *arrays: NDArray,
    aggregator: Callable = lambda x: np.array(x),
    **kw: dict[Any, Any],
) -> NDArray:
    """Computes transformations of cartesian product of all the elements in arrays.

    Args:
        arrays:  The arrays to product.
        aggregator: Callable to handle an item from product iterator.
            The first parameter of the callable is tuple of current product item.
            May return scalar or numpy ndarray.
        kw: keyword arguments to pass to aggregator

    Returns:
        ret: Numpy array with dimension of arrays and one more
            additional dimensions for their cartesian product.
    """
    res = np.stack([aggregator(x, **kw) for x in product(*arrays)])
    shape = tuple(map(len, arrays))
    if len(res.shape) > 1:  # the aggregation result is vector
        shape = shape + res.shape[1:]
    return res.reshape(shape)
