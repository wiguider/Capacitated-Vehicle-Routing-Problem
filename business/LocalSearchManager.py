from RandomMap import RandomMap


class LocalSearchManager:
    def __init__(self):
        self.random_routes = []
        self.cost_map = {}

    def get_random_routes(self, path):
        rm = RandomMap(path)
        rm.init_routes()
        rm.populate_routes_linehauls()
        rm.reset_routes_capacities()
        rm.populate_routes_backhauls()
        rm.calculate_cost()
        self.random_routes = rm.get_routes
