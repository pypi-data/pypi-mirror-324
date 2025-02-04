import typing as h
from multiprocessing.shared_memory import SharedMemory as shared_memory_t

import numpy as nmpy

array_t = nmpy.ndarray

LENGTH_DTYPE = nmpy.uint64


def NewSharedArray(
    array: array_t, /, *, name: str | None = None
) -> tuple[array_t, str, shared_memory_t]:
    """
    Buffer:
        - dtype: 1 byte
        - order: 1 byte
        - dimension: 1 byte
        - shape: dimension * 8 bytes (nmpy.uint64)
        - array content
    When not needed anymore, call close then unlink on raw.
    """
    assert array.ndim < 256

    shape = nmpy.array(array.shape, dtype=LENGTH_DTYPE)
    # assert shape.shape == (array.ndim,)
    # assert shape.nbytes == 8 * array.ndim

    while True:
        try:
            raw = shared_memory_t(
                name=name, create=True, size=shape.nbytes + array.nbytes + 3
            )
        except FileExistsError:
            name += chr(nmpy.random.randint(65, high=91))
        else:
            name = raw.name
            break

    enumeration_order: h.Literal["C", "F"]
    if array.flags["C_CONTIGUOUS"]:
        enumeration_order = "C"
    else:
        enumeration_order = "F"

    raw.buf[0] = ord(array.dtype.char)
    raw.buf[1] = ord(enumeration_order)
    raw.buf[2] = array.ndim

    for_shape = nmpy.ndarray(shape.shape, dtype=shape.dtype, buffer=raw.buf[3:])
    for_shape[...] = shape

    shaped = nmpy.ndarray(
        array.shape,
        dtype=array.dtype,
        order=enumeration_order,
        buffer=raw.buf[(shape.nbytes + 3) :],
    )
    shaped[...] = array

    return shaped, name, raw


def RetrievedNumpyArray(name: str, /) -> tuple[array_t, shared_memory_t]:
    """
    When not needed anymore, call close on raw.
    """
    raw = shared_memory_t(name)

    dtype_code = chr(raw.buf[0])
    enumeration_order: h.Literal["C", "F"] = chr(raw.buf[1])
    dimension = raw.buf[2]
    shape = nmpy.ndarray((dimension,), dtype=LENGTH_DTYPE, buffer=raw.buf[3:])

    return (
        nmpy.ndarray(
            shape,
            dtype=dtype_code,
            order=enumeration_order,
            buffer=raw.buf[(shape.nbytes + 3) :],
        ),
        raw,
    )
