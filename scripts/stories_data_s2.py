from stories_s2_p01 import STORIES_S2_P01
from stories_s2_p02 import STORIES_S2_P02
from stories_s2_p03 import STORIES_S2_P03
from stories_s2_p04 import STORIES_S2_P04
from stories_s2_p05 import STORIES_S2_P05
from stories_s2_p06 import STORIES_S2_P06
from stories_s2_p07 import STORIES_S2_P07
from stories_s2_p08 import STORIES_S2_P08
from stories_s2_p09 import STORIES_S2_P09

_PARTS = [
    (1, STORIES_S2_P01),
    (2, STORIES_S2_P02),
    (3, STORIES_S2_P03),
    (4, STORIES_S2_P04),
    (5, STORIES_S2_P05),
    (6, STORIES_S2_P06),
    (7, STORIES_S2_P07),
    (8, STORIES_S2_P08),
    (9, STORIES_S2_P09),
]

STORIES_S2 = []
for _part_num, _part in _PARTS:
    for _s in _part:
        STORIES_S2.append({**_s, "part": _part_num})
