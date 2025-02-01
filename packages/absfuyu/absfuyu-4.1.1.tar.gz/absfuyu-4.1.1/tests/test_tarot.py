"""
Test: Tarot

Version: 1.0.1
Date updated: 16/01/2025 (dd/mm/yyyy)
"""

# Library
###########################################################################
import pytest

from absfuyu.fun.tarot import Tarot, TarotCard


# Test
###########################################################################
def test_tarot():
    assert isinstance(Tarot().random_card(), TarotCard)
