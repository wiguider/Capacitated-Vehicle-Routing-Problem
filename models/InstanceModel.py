from random import shuffle

from models.Node import Node
from utils.InstanceReader import InstanceReader


class InstanceModel:
    def __init__(self, path):
        self.path = path
        self.clients_count = 0
        self.routes_count = 0
        self.rnd_nodes_ids = []
        self.linehaul_ids = []
        self.backhaul_ids = []
        self.max_capacity = 0
        self.nodes_list = []

    def line_to_node(self, line, i):
        splitted_x = line.split('   ')
        if splitted_x[2] == '0' and i > 0:
            capacity = splitted_x[3]
            node_type = 'backhaul'
            self.backhaul_ids.append(i)
        elif i > 0:
            capacity = splitted_x[2]
            node_type = 'linehaul'
            self.linehaul_ids.append(i)
        else:
            capacity = splitted_x[3]
            node_type = 'deposit'

        node = Node(i, int(splitted_x[0]), int(splitted_x[1]), int(capacity), node_type)
        return node

    def build_nodes_list(self, lines):
        i = 0
        for line in lines:
            node = self.line_to_node(line, i)
            self.nodes_list.append(node)
            i = i + 1

    def get_node_by_index(self, idx):
        for x in self.nodes_list:
            if x.get_index == int(idx):
                return x

    def build(self):
        ir = InstanceReader(self.path)
        self.clients_count = ir.get_clients_count()
        self.routes_count = ir.get_routes_count()
        self.max_capacity = ir.get_max_capacity()
        lines = ir.get_nodes()
        self.build_nodes_list(lines)
        shuffled = self.linehaul_ids + self.backhaul_ids
        shuffle(shuffled)
        self.rnd_nodes_ids = shuffled
