class Node(object):
    def __init__(self, l_child=None, r_child=None):
        self.l_child = l_child
        self.r_child = r_child

    def __repr__(self):
        return f"({self.l_child}, {self.r_child})"
