# https://docs.python.org/3/library/itertools.html
from itertools import chain
from string import ascii_uppercase, ascii_lowercase, digits


# Python does not offer the following base64 conversions conveniently
BASE64_DIGITS = ascii_uppercase + ascii_lowercase + digits + "+/"


def base64_decode(base64_string):
    """Return the int equal to BASE64_STRING."""
    result = 0
    for digit in base64_string:
        result *= 64
        result += BASE64_DIGITS.index(digit)
    return result


def base64_encode(number, length):
    """Return the base64 string equal to NUMBER padded to LENGTH."""
    # assert number < 64 ** length - 1
    result = []
    while number:
        result.append(BASE64_DIGITS[number % 64])
        number //= 64
    assert len(result) <= length
    result.append(BASE64_DIGITS[0] * (length - len(result)))
    return "".join(reversed(result))


def base64_sanitize(string):
    return "".join(filter(lambda x: x in BASE64_DIGITS, string))


def bfs(state, list_of_actions, keep_paths=False):
    visited = set()
    visited_path_pairs = {state: []}
    queue = [state]

    while queue:
        state = queue.pop(0)
        visited.add(state)
        path_so_far = visited_path_pairs.get(state) if keep_paths else None
        for action in list_of_actions:
            next_state = action(state)
            if next_state in visited or next_state in queue:
                continue
            queue.append(next_state)
            if keep_paths:
                visited_path_pairs[next_state] = path_so_far + [action]

    if keep_paths:
        return visited_path_pairs
    return visited


def flatten(list_of_lists):
    "Flatten one level of nesting"
    return chain.from_iterable(list_of_lists)


def poll(n, base64_string):
    polled, remaining = base64_string[:n], base64_string[n:]
    return base64_decode(reversed(polled)), remaining


def subtract_lists_of_offsets(list_1, list_2):
    """Helper function for computing kick translations, returns list_1 - list_2"""
    result = []
    for old_offsets, new_offsets in zip(list_1, list_2):
        old_row, old_column = old_offsets
        new_row, new_column = new_offsets
        result.append((old_row - new_row, old_column - new_column))
    return result
