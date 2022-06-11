import os
import random
import unittest
import tempfile
from typing import BinaryIO, List, Union
from bisect import bisect_left
import tqdm
from dichoseek import dichoseek


def generate_ordered_list_of_int(nb_to_generate, nb_bytes=4) -> List[int]:
    to_return = []

    for _ in range(nb_to_generate):
        to_return.append(random.randint(0, 2 ** (8 * nb_bytes) - 1))

    to_return.sort()
    return to_return


def write_binary_tmp_file(list_of_int: List[int], block_size) -> None:
    fd, path = tempfile.mkstemp()

    with os.fdopen(fd, "wb") as tmp:
        for e in list_of_int:
            tmp.write(e.to_bytes(block_size, byteorder="big"))

    return fd, path


def binary_search(
    a: List[int], x: int, lo: int = 0, hi: Union[None, int] = None
) -> int:
    """Used by `generate_elems_not_in_sorted_l` to test membership in oredered list."""
    if hi is None:
        hi = len(a)
    pos = bisect_left(a, x, lo, hi)  # find insertion position
    return pos if pos != hi and a[pos] == x else -1  # don't walk off the end


def generate_elems_not_in_sorted_l(
    nb_to_generate: int, l: List[int], nb_bytes: int = 4
) -> List[int]:
    to_return: List[int] = []
    while len(to_return) != nb_to_generate:
        e = l[0]
        while binary_search(l, e) != -1:
            e = random.randint(0, 2 ** (8 * nb_bytes) - 1)
        to_return.append(e)
    return to_return


def get_random_block_from_file(
    f: BinaryIO, nb_blocks: int, block_size: int
) -> bytes:
    random_block = random.randint(0, nb_blocks - 1)
    f.seek(random_block * block_size)
    return f.read(block_size)


def membership_testing(path: str, l: List[int], not_in_l: List[int]):
    """Calls `dichoseek` to figure out if all the
    elements of `l` are in the binary file at `path`
    and if all the elements in `not_in_l` are not.
    Calls to `dichoseek` are made twice: once by passing path
    and once by passing file to make sure both work.
    """
    for e in l:
        result = dichoseek(path, e, 4)
        if result != True:
            return False
        with open(path, "rb") as tmp:
            result = dichoseek(path, e, 4)
            if result != True:
                return False

    for e in not_in_l:
        result = dichoseek(path, e, 4)
        if result != False:
            return False
        with open(path, "rb") as tmp:
            result = dichoseek(path, e, 4)
            if result != False:
                return False
    return True


class TestDichoseek(unittest.TestCase):
    def test_block_size_check(self):
        """Tests that dichoseek raises ValueError
        if the size of the file is not a multiple of the block size.
        """
        l = [1]
        _, path = write_binary_tmp_file(l, 2)
        try:
            with self.assertRaises(ValueError):
                result = dichoseek(path, 1, 4)
        finally:
            os.remove(path)

    def test_out_of_range(self):
        l = [0, 1, 2]
        _, path = write_binary_tmp_file(l, 4)
        self.assertEqual(dichoseek(path, 3), False)

    def test_several_size_one_and_two_and_three_cases(self):
        """Test the sepcial cases of lists with only 1 or 2 elements."""
        for _ in range(100):
            nb_to_generate = random.randint(1, 3)
            l = generate_ordered_list_of_int(nb_to_generate)
            _, path = write_binary_tmp_file(l, 4)
            not_in_l = generate_elems_not_in_sorted_l(1000, l)

            try:
                self.assertEqual(membership_testing(path, l, not_in_l), True)
            finally:
                os.remove(path)

    def test_several_blocksize_four(self):
        """Test 10 files containing up to one million 4-byte integers."""
        for _ in tqdm.tqdm(range(10)):
            nb_to_generate = random.randint(1, 1e6)
            l = generate_ordered_list_of_int(nb_to_generate)
            _, path = write_binary_tmp_file(l, 4)
            not_in_l = generate_elems_not_in_sorted_l(1000, l)
            try:
                self.assertEqual(membership_testing(path, l, not_in_l), True)
            finally:
                os.remove(path)

    def test_bbchallenge_files(self):
        """`dichoseek` was built to help the https://github.com/bbchallenge/ project.
        Let's test that it does!
        """
        UNDECIDED_PATH = "tests/test_files/bb5_undecided_index"
        DECIDED_PATH = "tests/test_files/backward-reasoning-run-4b07b7719dbd-depth-300-minIndex-0-maxIndex-88664064"

        nb_undecided = os.path.getsize(UNDECIDED_PATH) // 4
        nb_decided = os.path.getsize(DECIDED_PATH) // 4

        with open(UNDECIDED_PATH, "rb") as f_undecided:
            with open(DECIDED_PATH, "rb") as f_decided:
                for _ in range(100):
                    random_undecided = int.from_bytes(
                        get_random_block_from_file(
                            f_undecided, nb_undecided, 4
                        ),
                        byteorder="big",
                    )
                    random_decided = int.from_bytes(
                        get_random_block_from_file(f_decided, nb_decided, 4),
                        byteorder="big",
                    )

                    self.assertEqual(
                        dichoseek(f_undecided, random_undecided), True
                    )
                    self.assertEqual(
                        dichoseek(f_undecided, random_decided), False
                    )
                    self.assertEqual(
                        dichoseek(f_decided, random_undecided), False
                    )
                    self.assertEqual(dichoseek(f_decided, random_decided), True)
