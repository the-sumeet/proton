from typing import Optional


def rreplace(s: str, old: str, new: str, occurrence: Optional[int] = 1):
    li = s.rsplit(old, occurrence)
    return new.join(li)
