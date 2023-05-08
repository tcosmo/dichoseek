# Dichoseek

Dichoseek tests the membership of a n-byte encoded integer in a sorted binary file consisting of a succession of n-byte integers.

The name comes from the fact that the algorithm is a dichotomy (binary search) using the file `seek` function.

## Instal

`pip install dichoseek`

## Basic usage

Assuming that you are looking for a 4-byte unsigned integer (you can change this assumption):

```python
from dichoseek import dichoseek
elem = 124
is_elem_in_file = dichoseek("path/to/file", elem)
```

Or using a file object:

```python
from dichoseek import dichoseek
elem = 124
with open("path/to/file", "rb") as f:
  is_elem_in_file = dichoseek(f, elem)
```

## Other parameters

- `block_size`: number of bytes per integer. We assume that the size of the file is a multiple of this `block_size`. Default is `4`.

- `block_interpretation_function` is the function that is used to transform bytes into `int`. Default is unsigned, big-endian parsing: `lambda b: int.from_bytes(b, byteorder="big")`.

