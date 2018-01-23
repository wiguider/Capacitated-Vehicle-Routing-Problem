from copy import copy

from RandomMap import RandomMap
from models.Node import Node
from models.Route import Route


class LocalSearchManager:
    def __init__(self, method):
        self._method = method
        self.random_map = None
        self.cost_map = {}

    def get_random_routes(self, file_path):
        rm = RandomMap(file_path)
        rm.init_routes()
        rm.populate_routes_linehauls()
        rm.populate_routes_backhauls()
        rm.calculate_cost()
        self.random_map = rm

    @staticmethod
    def exchange_elements_in_route(nodes, old_index, new_index):
        if len(nodes) > 2:
            nodes.insert(new_index, nodes.pop(old_index))
        return nodes

    def best_exchange(self):
        rm_instance_ref = copy(self.random_map)
        rm_instance = copy(self.random_map)
        allNodes = []
        allnodesStock = []
        assert isinstance(rm_instance_ref, RandomMap)
        for route in rm_instance_ref.get_routes:
            for node in route.get_nodes:
                assert isinstance(node, Node)
                if node.get_type != "deposit":
                    allnodesStock.append(node)
                allNodes.append(node)
        allnodesr = copy(allNodes)
        for s in allnodesStock:
            for i in range(0, len(allnodesr) - 1):
                if allnodesr[i].get_index != 0:
                    s_index = allnodesr.index(s)
                    allnodesr = self.exchange_elements_in_route(allnodesr, s_index, s_index + 1)
                    # TODO:build map from allnodesr (0, 1, 2, 3, 4, 0, 0, 5, 6, 7, 0) + compute cost

                    if (s == allnodesr[-2]):
                        break
            allnodesr = allNodes

    # TODO: Relocate element in the same route,
    # TODO: Relocate element in another route,
    # TODO: Exchange elements in different routes
    # TODO: Check linehaul, backhaul, and capacity conditions

    def build_map_from_list(self, lista):
        listo = []
        listi = []
        routes_map = []
        for i in range(0, len(lista)):
            listo.append(lista[i])
            if lista[i].get_index == 0 and lista[i + 1].get_index == 0:
                listi.append(listo)
                listo = []

        for rn in listi:
            route = Route()
            for n in rn:
                route.add_node(n)
            if route.is_route_valid():
                return False
            routes_map.append(route)
        cost = 0
        for route in routes_map:
            cost += route.get_cost
        rm = RandomMap()
        rm.set_routes(routes_map)
        rm.set_cost(cost)
        self.cost_map[cost] = rm
        return True
