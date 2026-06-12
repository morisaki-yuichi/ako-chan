from stories_s3_p01 import STORIES_S3_P01
from stories_s3_p02 import STORIES_S3_P02
from stories_s3_p03 import STORIES_S3_P03
from stories_s3_p04 import STORIES_S3_P04
from stories_s3_p05 import STORIES_S3_P05
from stories_s3_p06 import STORIES_S3_P06
from stories_s3_p07 import STORIES_S3_P07
from stories_s3_p08 import STORIES_S3_P08
from stories_s3_p09 import STORIES_S3_P09
from stories_s3_p10 import STORIES_S3_P10
from stories_s3_p11 import STORIES_S3_P11

_PARTS = [
    STORIES_S3_P01,
    STORIES_S3_P02,
    STORIES_S3_P03,
    STORIES_S3_P04,
    STORIES_S3_P05,
    STORIES_S3_P06,
    STORIES_S3_P07,
    STORIES_S3_P08,
    STORIES_S3_P09,
    STORIES_S3_P10,
    STORIES_S3_P11,
]

STORIES_S3 = []
_ep = 1
for _part_num, _part in enumerate(_PARTS, 1):
    for _s in _part:
        STORIES_S3.append({
            "ep": _ep,
            "part": _part_num,
            "title": _s["title"],
            "text": _s["text"],
        })
        _ep += 1
