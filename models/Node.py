class Node:
    def __init__(self, index, x, y, capacity, node_type):
        assert isinstance(index, int)
        self._index = index  # Node index
        assert isinstance(x, int)
        self._x = x  # X coordinate
        assert isinstance(y, int)
        self._y = y  # Y coordinate
        assert isinstance(capacity, int)
        self._capacity = capacity  # Node capacity
        assert isinstance(node_type, str)
        self._type = node_type  # Node type (linehaul or backhaul)

    def get_coords(self):
        return [int(self._x), int(self._y)]

    @property
    def get_index(self):
        assert isinstance(self._index, int)
        return self._index

    @property
    def get_x(self):
        assert isinstance(self._x, int)
        return self._x

    @property
    def get_y(self):
        assert isinstance(self._y, int)
        return self._y

    @property
    def get_type(self):
        assert isinstance(self._type, str)
        return self._type

    @property
    def get_capacity(self):
        assert isinstance(self._capacity, int)
        return self._capacity

    def __repr__(self):
        return "\n[x=" + str(self._x) + " y=" + str(self._y) + " capacity=" + str(self._capacity) + " index=" + str(
                self._index) + " type=" + str(
                self._type) + "]"

    def __cmp__(self, other):
        return int(self._x) == int(other.get_x()) and int(self._y) == int(other.get_y())

    def __eq__(self, other):
        return int(self._x) == int(other.get_x()) and int(self._y) == int(other.get_y())
