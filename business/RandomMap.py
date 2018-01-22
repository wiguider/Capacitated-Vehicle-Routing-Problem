from models.InstanceModel import InstanceModel
from models.Route import Route


class RandomMap:
    def __init__(self, path):
        self._instance = InstanceModel(path)
        self._instance.build()
        self._vehicle_capacity = int(self._instance.max_capacity)
        self._routes = []
        self.cost = 0.0

    def init_routes(self):
        """
        Adds the deposit and a first linehaul node to each route
        :return:
        """
        for i in range(0, int(self._instance.routes_count)):
            route = Route()
            route.set_index(i)
            route.add_node(self._instance.nodes_list[0])
            route.max_linehaul_capacity = self._vehicle_capacity
            route.max_backhaul_capacity = self._vehicle_capacity
            for x in self._instance.rnd_nodes_ids:
                node = self._instance.get_node_by_index(x)
                if len(self._instance.linehaul_ids) > 0:
                    if node.get_type == 'linehaul' and node.get_index in self._instance.linehaul_ids and node.get_capacity <= self._vehicle_capacity:
                        route.add_node(node)
                        self._instance.linehaul_ids.pop(self._instance.linehaul_ids.index(x))
                        self._routes.append(route)
                        break

    def reset_routes_capacities(self):
        for route in self._routes:
            route.max_backhaul_capacity = self._vehicle_capacity

    def populate_routes_linehauls(self):
        for route in self._routes:
            for x in self._instance.rnd_nodes_ids:
                node = self._instance.get_node_by_index(x)
                if len(self._instance.linehaul_ids) > 0:
                    if node.get_type == 'linehaul' and node.get_index in self._instance.linehaul_ids and node.get_capacity <= route.max_linehaul_capacity:
                        route.add_node(node)
                        self._instance.linehaul_ids.pop(self._instance.linehaul_ids.index(x))

        if len(self._instance.linehaul_ids) > 0:
            self.populate_routes_linehauls()

    def populate_routes_backhauls(self):
        for route in self._routes:
            for x in self._instance.rnd_nodes_ids:
                node = self._instance.get_node_by_index(x)
                if len(self._instance.backhaul_ids) > 0:
                    if node.get_type == 'backhaul' and node.get_index in self._instance.backhaul_ids and node.get_capacity <= route.max_backhaul_capacity:
                        route.add_node(node)
                        self._instance.backhaul_ids.pop(self._instance.backhaul_ids.index(x))
        if len(self._instance.backhaul_ids) > 0:
            self.populate_routes_backhauls()
        for route in self._routes:
            route.add_deposit_at_last()

    def calculate_cost(self):
        for route in self._routes:
            self.cost += route.get_cost

    @property
    def get_routes(self):
        return self._routes

    def __repr__(self):
        return "\n{ " \
               "\nroutes: " + str(self.get_routes) + ", " +\
               "\ntotal_cost: " + str(self.cost) + "}"
