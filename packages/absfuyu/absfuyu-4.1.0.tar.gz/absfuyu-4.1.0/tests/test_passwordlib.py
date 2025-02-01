"""
Test: Passwordlib

Version: 1.1.1
Date updated: 19/04/2024 (dd/mm/yyyy)
"""

from itertools import combinations_with_replacement

import pytest

try:  # [res] feature
    import absfuyu_res
except ImportError:
    absfuyu_res = pytest.importorskip("absfuyu_res")

from absfuyu.extensions.dev.passwordlib import Password
from absfuyu.general.data_extension import Text

# def test_generate_password():
#     test = [password_check(Password.generate_password()) for _ in range(100)]
#     assert all(test)


def test_generate_password_matrix():
    num_of_test = 1000

    def check(value: dict) -> int:
        return sum([1 for x in value.values() if x > 0])

    out = []
    check_matrix = list(
        set(combinations_with_replacement([True, False, True, False, True, False], 3))
    )
    for x in check_matrix:
        include_number, include_special, include_uppercase = x
        check_value = sum(x) + 1

        test = [
            Text(
                Password.generate_password(
                    include_number=include_number,
                    include_special=include_special,
                    include_uppercase=include_uppercase,
                )
            ).analyze()
            for _ in range(num_of_test)
        ]
        test = list(set(map(check, test)))
        if len(test) == 1:
            out.append(test[0] == check_value)
        else:
            # assert False
            raise AssertionError()

    assert all(out)
