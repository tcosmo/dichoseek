from multiprocessing.sharedctypes import Value
import os
from typing import Callable, Union, BinaryIO


def dichoseek(
    filename_or_binary_file: Union[str, BinaryIO],
    elem_to_find: int,
    block_size: int = 4,
    block_interpretation_function: Callable[
        [bytes], int
    ] = lambda b: int.from_bytes(b, byteorder="big"),
) -> bool:
    """
    Returns True if the int `elem_to_find` is present in the sorted binary file specified
    by `filename_or_binary_file`. Implements a dichotomy using file `seek` operations.

    Args:
        filename_or_binary_file: File name or file object of binary-opened file.
        elem_to_find: The element to find in the file.
        block_size: Number of bytes in a block that will be interpreted as an integer.
                    By default it is 4 (32-bit integer).
        block_interpretation_function: A function turning a block of `block_size` bytes into an int.


    Returns:
        True iff `elem_to_find` is present in the binary file.

    Raises:
        OSError: is failed to open filename_or_binary_file (if it was a str).
        ValueError: if size of the file is not a multiple of the block size.

    """

    f: BinaryIO = filename_or_binary_file
    to_close = False
    if isinstance(f, str):
        f = open(filename_or_binary_file, "rb")
        to_close = True

    f.seek(0, os.SEEK_END)
    file_size = f.tell()
    f.seek(0)

    if file_size % block_size != 0:
        if to_close:
            f.close()
        raise ValueError(
            f"The size of the file ({file_size}) is not a multiple of the given block size ({block_size})."
        )

    nb_blocks = file_size // block_size
    beg, end = 0, nb_blocks

    while beg <= end:
        middle = (beg + end) // 2
        f.seek(middle * block_size)
        raw_bytes = f.read(block_size)
        corresponding_int = block_interpretation_function(raw_bytes)

        if corresponding_int == elem_to_find:
            if to_close:
                f.close()
            return True
        elif corresponding_int > elem_to_find:
            end = middle - 1
        else:
            beg = middle + 1

    if to_close:
        f.close()
    return False
