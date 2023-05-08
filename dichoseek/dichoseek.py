from multiprocessing.sharedctypes import Value
import os
from typing import Callable, Union, BinaryIO


def dichoseek(
    filename_or_binary_file: Union[str, BinaryIO],
    elem_to_find: int,
    block_size: int = 4,
    block_interpretation_function: Callable[[bytes], int] = lambda b: int.from_bytes(
        b, byteorder="big"
    ),
    begin_at_byte: int = 0,
    end_at_byte: Union[int, None] = None,
) -> bool:
    """
    Returns True iff the int `elem_to_find` is present in the sorted binary file specified
    by `filename_or_binary_file`. Implements a dichotomy using file `seek` operations.

    Args:
        filename_or_binary_file: File name or file object of binary-opened file.
        elem_to_find: The element to find in the file.
        block_size: Number of bytes in a block that will be interpreted as an integer.
                    By default it is 4 (32-bit integer).
        block_interpretation_function: A function turning a block of `block_size` bytes into an int.
        begin_at_byte: offset to start the search at, default is 0
        end_at_byte: offset to end the search at, default is None = EOF

    Returns:
        True iff `elem_to_find` is present in the binary file.

    Raises:
        OSError: is failed to open filename_or_binary_file (if it was a str).
        ValueError: if size of the file is not a multiple of the block size.

    """
    return (
        dichoseek_index(
            filename_or_binary_file,
            elem_to_find,
            block_size,
            block_interpretation_function,
            begin_at_byte,
            end_at_byte,
        )
        is not None
    )


def get_chunk_size(file_size: int, begin_at_byte: int, end_at_byte: Union[int, None]):
    """Returns the size of a file's chunk.

    Args:
        file_size (int): file size
        begin_at_byte (Union[int, None]): begin of chunk, None if 0
        end_at_byte (Union[int, None]): end of chunk, `None if file_size`
    """
    end = end_at_byte if end_at_byte is not None else file_size
    begin = begin_at_byte
    return end - begin


def dichoseek_index(
    filename_or_binary_file: Union[str, BinaryIO],
    elem_to_find: int,
    block_size: int = 4,
    block_interpretation_function: Callable[[bytes], int] = lambda b: int.from_bytes(
        b, byteorder="big"
    ),
    begin_at_byte: int = 0,
    end_at_byte: Union[int, None] = None,
) -> Union[int, None]:
    """
    Returns None if the int `elem_to_find` is not present in the sorted binary file specified
    by `filename_or_binary_file`. Otherwise, it returns an index where it is present.
    Implements a dichotomy using file `seek` operations.

    Args:
        filename_or_binary_file: File name or file object of binary-opened file.
        elem_to_find: The element to find in the file.
        block_size: Number of bytes in a block that will be interpreted as an integer.
                    By default it is 4 (32-bit integer).
        block_interpretation_function: A function turning a block of `block_size` bytes into an int.
        begin_at_byte: offset to start the search at, default is 0
        end_at_byte: offset to end the search at, default is None = EOF

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
    chunk_end = file_size

    if end_at_byte is not None:
        chunk_end = end_at_byte

    # Rewind
    f.seek(begin_at_byte)

    chunk_size = get_chunk_size(file_size, begin_at_byte, end_at_byte)

    if chunk_size % block_size != 0:
        if to_close:
            f.close()
        raise ValueError(
            f"The size of the chunk ({chunk_size}) is not a multiple of the given block size ({block_size})."
        )

    nb_blocks = chunk_size // block_size
    beg, end = 0, nb_blocks

    while beg < end:
        middle = (beg + end) // 2
        assert begin_at_byte + middle * block_size < chunk_end
        f.seek(begin_at_byte + middle * block_size)
        raw_bytes = f.read(block_size)
        corresponding_int = block_interpretation_function(raw_bytes)
        if corresponding_int == elem_to_find:
            if to_close:
                f.close()
            return middle
        elif corresponding_int > elem_to_find:
            end = middle
        else:
            beg = middle + 1

    if to_close:
        f.close()
    return None
