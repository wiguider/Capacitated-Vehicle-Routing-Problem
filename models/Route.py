from models.Node import Node
from utils import DistanceCalculator


class Route:
    def __init__(self):
        self._nodes = []  # List of the nodes in the route
        self._cost = 0.0  # Cost of the route

        self._delivery_load = 0  # Delivery load
        self._pickup_load = 0  # Pickup load

        self.max_capacity = 0

    def add_node(self, node):
        """
        Adds the given node to the list of nodes
        :param node: models.Node
        :return: None
        """
        if len(self._nodes) > 0:
            self.check_node(node)
        self._nodes.append(node)

    # TODO: Add node at position, Relocate element in another route,
    # TODO: Exchange elements at positions (i,j) in route, Exchange elements in different routes

    def check_node(self, node):
        """
        According to the type of the last node,
        updates the delivery/pickup load and updates the route's cost
        :param node: models.Node
        :return: None
        """
        if node.get_type == 'linehaul':
            self._delivery_load += node.get_capacity
        elif node.get_type == 'backhaul':
            self._pickup_load += node.get_capacity
        last_node = self._nodes[-1]
        assert isinstance(last_node, Node)
        self._cost += DistanceCalculator.euclidean_distance(last_node.get_coords(), node.get_coords())

    def add_deposit_at_last(self):
        node = self._nodes[0]
        self._nodes.append(node)
        last_node = self._nodes[-1]
        self._cost += DistanceCalculator.euclidean_distance(last_node.get_coords(), node.get_coords())

    def add_node_at_position(self, node, position):
        # TODO: Check linehaul/backhaul condition
        self._nodes.insert(position, node)

    def delete_node_at_position(self, position):
        self._nodes.pop(position)

    @property
    def get_nodes(self):
        return self._nodes

    @property
    def get_cost(self):
        return self._cost

    @property
    def get_delivery_load(self):
        return self._delivery_load

    @property
    def get_pickup_load(self):
        return self._pickup_load

    def __repr__(self):
        return "\n{nodes: " + str(self.get_nodes) + "\nmax_capacity: " + str(self.max_capacity) + "\ncost: " + str(
            self.get_cost) + "}"
