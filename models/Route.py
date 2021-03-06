import re
import sys

from models.Node import Node
from utils import DistanceCalculator



class Route:
    def __init__(self):
        self._index = -1  # Index of the route
        self._nodes = []  # List of the nodes in the route
        self._cost = 0.0  # Cost of the route
        self._delivery_load = 0  # Delivery load
        self._pickup_load = 0  # Pickup load

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
        assert isinstance(node, Node)
        if len(self._nodes) > 0:
            self.check_node(node)
        self._nodes.append(node)

    def check_node(self, node):
        """
        According to the type of the last node,
        updates the delivery/pickup load and updates the route's cost
        :param node: models.Node
        :return: None
        """
        assert isinstance(node, Node)
        if node.get_type == 'linehaul':
            self._delivery_load += node.get_capacity
            self.max_linehaul_capacity = self.max_linehaul_capacity - node.get_capacity
        elif node.get_type == 'backhaul':
            self._pickup_load += node.get_capacity
            self.max_backhaul_capacity = self.max_backhaul_capacity - node.get_capacity

        last_node = self._nodes[-1]
        assert isinstance(last_node, Node)
        self._cost += DistanceCalculator.euclidean_distance(last_node.get_coords(), node.get_coords())
        self._cost = round(self._cost, 2)

    def add_deposit_at_last(self):
        """
        Adds the deposit node at the end of the route
        :return:
        """
        node = self._nodes[0]
        self._nodes.append(node)
        last_node = self._nodes[-1]
        self._cost += DistanceCalculator.euclidean_distance(last_node.get_coords(), node.get_coords())
        self._cost = round(self._cost, 2)

    def add_node_at_position(self, node, position):
        """
        Adds the given node at the given position and update the cost of the route
        :param node:
        :param position:
        :return:
        """

        is_valid = False
        assert isinstance(position, int)
        assert isinstance(node, Node)
        last_node = self._nodes[position - 1]
        assert isinstance(last_node, Node)
        if node.get_type == 'linehaul':
            if last_node.get_type == 'linehaul':
                if node.get_capacity <= self.max_linehaul_capacity:
                    self._nodes.insert(position, node)
                    self._delivery_load += node.get_capacity
                    self.max_linehaul_capacity = self.max_linehaul_capacity - node.get_capacity
                    is_valid = True
        else:
            next_node = self._nodes[position + 1]
            assert isinstance(next_node, Node)
            if next_node.get_type == 'backhaul' or next_node.get_type == 'deposit':
                if node.get_capacity <= self.max_backhaul_capacity:
                    self._nodes.insert(position, node)
                    self._pickup_load += node.get_capacity
                    self.max_backhaul_capacity = self.max_backhaul_capacity - node.get_capacity
                    is_valid = True
        self.update_cost()
        return is_valid

    def delete_node_at_position(self, position):
        """
        Deletes a node at the given position and updates the capacities
        :param position:
        :return:
        """
        assert isinstance(position, int)
        node = self._nodes[position]
        assert isinstance(node, Node)
        self._nodes.pop(position)
        if node.get_type == 'linehaul':
            self._delivery_load -= node.get_capacity
            self.max_linehaul_capacity = self.max_linehaul_capacity + node.get_capacity

        elif node.get_type == 'backhaul':
            self._pickup_load -= node.get_capacity
            self.max_backhaul_capacity = self.max_backhaul_capacity + node.get_capacity
        self.update_cost()
        return node

    @property
    def get_index(self):
        return self._index

    def set_index(self, index):
        """
        Sets the index of this route
        :type index: int
        """
        assert isinstance(index, int)
        self._index = index

    @property
    def get_nodes(self):
        return self._nodes

    @property
    def get_cost(self):
        return self._cost

    @property
    def get_delivery_load(self):
        return self._delivery_load

    def set_delivery_load(self, delivery_load):
        self._delivery_load = delivery_load

    @property
    def get_pickup_load(self):
        return self._pickup_load

    def set_pickup_load(self, pickup_load):
        self._pickup_load = pickup_load

    def update_cost(self):
        """
        Recalculates and updates the routes' cost
        :return:
        """
        cost = 0
        for i in range(0, len(self._nodes) - 1):
            last_node = self._nodes[i - 1]
            assert isinstance(last_node, Node)
            node = self._nodes[i]
            assert isinstance(node, Node)

            cost += DistanceCalculator.euclidean_distance(last_node.get_coords(), node.get_coords())
        self._cost = round(cost, 2)

    def is_route_valid(self):
        seq = self.get_nodes_seq()
        match = re.match(r'(L+B*){1}', seq)
        if hasattr(match, 'groups'):
            match_groups = match.groups()
            if len(match_groups[0]) == len(seq):
                return True and self.check_capacity()
        return False

    def check_capacity(self):
        lcapacity = 0
        bcapacity = 0
        for n in self._nodes:
            if n.get_type == 'linehaul':
                lcapacity += n.get_capacity
            elif n.get_type == 'backhaul':
                bcapacity += n.get_capacity
        if self._nodes[0].get_capacity < lcapacity or self._nodes[0].get_capacity < bcapacity:
            return False
        self.max_linehaul_capacity = self._nodes[0].get_capacity - lcapacity
        self.max_backhaul_capacity = self._nodes[0].get_capacity - bcapacity
        return True

    def get_nodes_seq(self):
        seq = ''
        nodes = self.get_nodes
        for i in range(1, len(nodes) - 1):
            if bool(nodes[i].get_type == 'linehaul'):
                seq += 'L'
            else:
                seq += 'B'
        return seq

    def __repr__(self):
        return "\n{ " \
               "\nindex: " + str(self.get_index) + ", " + \
               "\nnodes: " + str(self.get_nodes) + ", " + \
               "\nmax_linehaul_capacity: " + str(self.max_linehaul_capacity) + ", " + \
               "\nmax_backhaul_capacity: " + str(self.max_backhaul_capacity) + ", " + \
               "\ndelivery_load: " + str(self._delivery_load) + "," + \
               "\npickup_load: " + str(self._pickup_load) + "," + \
               "\ncost: " + str(self.get_cost) + "}"
