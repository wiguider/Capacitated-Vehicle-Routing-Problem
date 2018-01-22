from models.Node import Node
from utils import DistanceCalculator


class Route:
    def __init__(self):
        self._nodes = []  # List of the nodes in the route
        self._cost = 0.0  # Cost of the route

        self._delivery_load = 0  # Delivery load
        self._pickup_load = 0  # Pickup load
        # max_capacity is deprecated now we are using max_linehaul_capacity and max_backhaul_capacity
        self.max_capacity = 0
        # Update: it's better to separate max capacities
        # instead of resetting one variable because it will be useful when updating routes
        self.max_linehaul_capacity = 0
        self.max_backhaul_capacity = 0

    def add_node(self, node):
        """
        Adds the given node to the list of nodes
        :param node: models.Node
        :return: None
        """
        if len(self._nodes) > 0:
            self.check_node(node)
        self._nodes.append(node)

    # TODO: Relocate element in another route,
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
            self.max_linehaul_capacity = self.max_linehaul_capacity - node.get_capacity
        elif node.get_type == 'backhaul':
            self._pickup_load += node.get_capacity
            self.max_backhaul_capacity = self.max_backhaul_capacity - node.get_capacity

        last_node = self._nodes[-1]
        assert isinstance(last_node, Node)
        self._cost += DistanceCalculator.euclidean_distance(last_node.get_coords(), node.get_coords())

    def add_deposit_at_last(self):
        node = self._nodes[0]
        self._nodes.append(node)
        last_node = self._nodes[-1]
        self._cost += DistanceCalculator.euclidean_distance(last_node.get_coords(), node.get_coords())

    def add_node_at_position(self, node, position):
        # TODO: Check capacity condition
        assert isinstance(position, int)
        assert isinstance(node, Node)
        last_node = self._nodes[position - 1]
        assert isinstance(last_node, Node)
        if node.get_type == 'linehaul':
            if last_node.get_type == 'linehaul':
                # TODO: Update cost
                self._nodes.insert(position, node)
                self._delivery_load += node.get_capacity
                self.max_linehaul_capacity = self.max_linehaul_capacity - node.get_capacity
        else:
            next_node = self._nodes[position + 1]
            assert isinstance(next_node, Node)
            if next_node.get_type == 'backhaul' or next_node.get_type == 'deposit':
                # TODO: Update cost
                self._nodes.insert(position, node)
                self._pickup_load += node.get_capacity
                self.max_backhaul_capacity = self.max_backhaul_capacity - node.get_capacity

    def delete_node_at_position(self, position):
        """
        Deletes a node at the given position and updates the capacities
        :param position:
        :return:
        """
        node = self._nodes[position]
        assert isinstance(node, Node)
        self._nodes.pop(position)
        if node.get_type == 'linehaul':
            self._delivery_load -= node.get_capacity
            self.max_linehaul_capacity = self.max_linehaul_capacity + node.get_capacity

        elif node.get_type == 'backhaul':
            self._pickup_load -= node.get_capacity
            self.max_backhaul_capacity = self.max_backhaul_capacity + node.get_capacity
        # TODO: Update cost

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
        return "\n{nodes: " + str(self.get_nodes) + "\nmax_linehaul_capacity: " + str(self.max_linehaul_capacity) + "\nmax_backhaul_capacity: " + str(
                self.max_backhaul_capacity) + "\ncost: " + str(
                self.get_cost) + "}"
