__author__ = 'oakfang'

from cain.jsonable import raw_json
from jsonable_dummys import PACKS, FEATS
import pytest


@pytest.mark.parametrize(('path', 'end_value'),
                         [([0, "name"], "Black"),
                          ([0, "members", 2, "score"], 70)])
def test_packs(path, end_value):
    walk = raw_json(PACKS)
    for step in path:
        walk = walk[step]
    assert walk == end_value


@pytest.mark.parametrize(('path', 'end_value'),
                         [([0, "name"], "Alcohol"),
                          ([2, "broperty", "code"], "knight"),
                          ([0, "feats", 0, "worth"], 3)])
def test_feats(path, end_value):
    walk = raw_json(FEATS)
    for step in path:
        walk = walk[step]
    assert walk == end_value