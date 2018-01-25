from copy import copy

from RandomMap import RandomMap
from models.Node import Node
from models.Route import Route


class LocalSearchManager:
    def __init__(self):
        self.random_map = None
        self.cost_map = {}
        self.file_name = ''
        self.last_cost = 0.0

    def get_random_routes(self, file_path):
        rm = RandomMap(file_path)
        rm.init_routes()
        rm.populate_routes_linehauls()
        rm.populate_routes_backhauls()
        rm.calculate_cost()
        self.file_name = rm.file_name
        self.random_map = rm

    @staticmethod
    def exchange_elements_in_route(nodes, old_index, new_index):
        if len(nodes) > 2:
            nodes.insert(new_index, nodes.pop(old_index))
        return nodes

    def best_exchange(self):
        rm_instance_ref = copy(self.random_map)
        rm_instance = copy(self.random_map)
        self.cost_map[rm_instance.cost] = rm_instance
        allNodes = []
        allnodesStock = []
        assert isinstance(rm_instance_ref, RandomMap)
        for route in rm_instance_ref.get_routes:
            for node in route.get_nodes:
                assert isinstance(node, Node)
                allNodes.append(node)
                if node.get_type != "deposit":
                    allnodesStock.append(node)

        allnodesr = copy(allNodes)
        for s in allnodesStock:
            for i in range(0, len(allnodesr) - 1):
                if allnodesr[i].get_index != 0:
                    s_index = allnodesr.index(s)

                    if allnodesr[s_index + 1].get_index != 0:

                        allnodesr = self.exchange_elements_in_route(allnodesr, s_index, s_index + 1)
                        # Build map from allnodesr (0, 1, 2, 3, 4, 0, 0, 5, 6, 7, 0) + compute cost
                        self.build_map_from_list(allnodesr)
                    else:
                        allnodesr = self.exchange_elements_in_route(allnodesr, s_index, s_index + 3)
                        # Build map from allnodesr (0, 1, 2, 3, 4, 0, 0, 5, 6, 7, 0) + compute cost
                        self.build_map_from_list(allnodesr)
                    if s == allnodesr[-2]:
                        break
            allnodesr = allNodes
        min_cost = min(self.cost_map.keys())
        print self.cost_map[min_cost]
        print 'GAP: ', self.calculate_gap(min_cost), '% '
        print 'Served clients: ', len(allnodesStock)
        return self.cost_map[min_cost]

    def first_exchange(self):
        rm_instance_ref = copy(self.random_map)
        rm_instance = copy(self.random_map)
        allNodes = []
        allnodesStock = []
        self.cost_map = {}
        assert isinstance(rm_instance_ref, RandomMap)
        for route in rm_instance_ref.get_routes:
            for node in route.get_nodes:
                assert isinstance(node, Node)
                allNodes.append(node)
                if node.get_type != "deposit":
                    allnodesStock.append(node)
        self.last_cost = rm_instance.cost
        allnodesr = copy(allNodes)
        for s in allnodesStock:
            for i in range(0, len(allnodesr) - 1):
                if allnodesr[i].get_index != 0:
                    s_index = allnodesr.index(s)

                    if allnodesr[s_index + 1].get_index != 0:

                        allnodesr = self.exchange_elements_in_route(allnodesr, s_index, s_index + 1)
                        # Build map from allnodesr (0, 1, 2, 3, 4, 0, 0, 5, 6, 7, 0) + compute cost
                        self.build_map_from_list(allnodesr)
                    else:
                        allnodesr = self.exchange_elements_in_route(allnodesr, s_index, s_index + 3)
                        # Build map from allnodesr (0, 1, 2, 3, 4, 0, 0, 5, 6, 7, 0) + compute cost
                        self.build_map_from_list(allnodesr)
                    costs = self.cost_map.keys()
                    if costs[-1] < self.last_cost:
                        return self.cost_map[costs[-1]]

                    if s == allnodesr[-2]:
                        break
            allnodesr = allNodes

        print rm_instance
        print 'GAP: ', self.calculate_gap(rm_instance.cost), '% '
        print 'Served clients: ', len(allnodesStock)
        return rm_instance

    # TODO: Relocate element in the same route,
    # TODO: Relocate element in another route,

    def build_map_from_list(self, lista):
        listo = []
        listi = []
        routes_map = []
        for i in range(0, len(lista)):
            listo.append(lista[i])
            if i != len(lista) - 1:
                if lista[i].get_index == 0 and lista[i + 1].get_index == 0:
                    listi.append(listo)
                    listo = []
            if lista[i].get_index == 0 and i == len(lista) - 1:
                listi.append(listo)
                listo = []
        c = 0
        for rn in listi:
            route = Route()
            for n in rn:
                route.add_node(n)
            if not route.is_route_valid():
                return False

            route.set_index(c)
            routes_map.append(route)
            c += 1
        if len(routes_map) != len(self.random_map.get_routes):
            return False

        cost = 0
        for route in routes_map:
            cost += route.get_cost

        rm = RandomMap()
        rm.set_routes(routes_map)
        rm.set_cost(cost)
        rm.file_name = self.file_name
        self.cost_map[cost] = rm

        return True

    def execute(self, method):
        options = {
            'first_exchange': self.first_exchange,
            'best_exchange': self.best_exchange,
            #           'first_relocate': first_relocate,
            #          'best_relocate': best_relocate,
        }
        options[method]()

    def get_ref_cost(self):
        f = open('RPA_Solutions/Detailed_Solution_' + self.file_name, "r")
        lines = f.readlines()
        lines = [x.rstrip() for x in lines]
        cost_line = lines[8].split(' = ')
        return float(cost_line[1])

    def calculate_gap(self, my_cost):
        ref_cost = self.get_ref_cost()
        assert isinstance(ref_cost, float)
        assert isinstance(my_cost, float)
        return round((float(my_cost - ref_cost) / ref_cost) * 100, 2)
