# Dichoseek

Dichoseek tests the membership of a n-byte encoded integer in a sorted binary file consisted of a succession of n-byte integers.

Assuming that you are looking for 4-byte unsigned integers (you can change this assumption):

```python
from dichoseek import dichoseek
elem = 124
is_elem_in_file = dichoseek("path/to/file", elem)
```

Or:

```python
from dichoseek import dichoseek
elem = 124
with open("path/to/file", "rb") as f:
  is_elem_in_file = dichoseek(f, elem)
```
