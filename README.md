# Dichoseek

Dichoseek tests the membership of a n-byte encoded integer in a sorted binary file consisted of a succession of n-byte integers.

Assuming that you are looking for 4-byte unsigned integers (you can change this assumption):

### Using a path

```python
from dichoseek import dichoseek
elem = 124
is_elem_in_file = dichoseek("path/to/file", elem)
```

### Or a file object

```python
from dichoseek import dichoseek
elem = 124
with open("path/to/file", "rb") as f:
  is_elem_in_file = dichoseek(f, elem)
```

## Other parameters

### Block size, default is 4 (number of bytes per number)

```python
is_elem_in_file = dichoseek("path/to/file", elem, block_size = 4)
```

### Block-interpreting function

`block_interpretation_function` is the function that is used to transform bytes into `int`. Default is big-endian parsing: `lambda b: int.from_bytes(b, byteorder="big")`.

```python
is_elem_in_file = dichoseek("path/to/file", elem, 
                            block_interpretation_function = 
                            lambda b: int.from_bytes(b, byteorder="big")
```