import re

import localbench


def test_version_looks_like_a_version_number():
    assert re.fullmatch(r"\d+\.\d+\.\d+", localbench.__version__)
