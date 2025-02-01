import pytest

try:  # [beautiful] feature
    import rich  # type: ignore
except ImportError:
    rich = pytest.importorskip("rich")

from absfuyu.extensions import beautiful as bu


class TestBeautiful:
    def test_beau(self):
        assert bu.demo() is None
