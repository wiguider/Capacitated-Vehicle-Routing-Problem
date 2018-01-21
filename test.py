from business.RandomMap import RandomMap
from models.InstanceModel import InstanceModel


def main():
    # im = InstanceModel("Instances/A1.txt")
    # im.build()
    # print im.linehaul_ids
    # print im.backhaul_ids
    # print im.rnd_nodes_ids
    # print im.nodes_list
    rm = RandomMap("Instances/A1.txt")
    rm.init_routes()
    rm.populate_routes_linehauls()
    rm.reset_routes_capacities()
    rm.populate_routes_backhauls()
    rm.calculate_cost()
    print rm.get_routes
    print rm.cost


if __name__ == '__main__':
    main()
