from __future__ import annotations  # for node datatypes, should be able to remove w/ py3.10

from typing import Union, Optional


class Node(object):
    def __init__(self, l_child: Optional[Union[str, Node]] = None, r_child: Optional[Union[str, Node]] = None):
        self.l_child: Optional[Union[str, Node]] = l_child
        self.r_child: Optional[Union[str, Node]] = r_child

    def __repr__(self):
        return f"({self.l_child}, {self.r_child})"
