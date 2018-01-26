import glob
import os

from business.LocalSearchManager import LocalSearchManager
from business.RandomMap import RandomMap
from models.Route import Route
from utils.FileWriter import FileWriter

rnd_maps_list = []


def ensure_dir(file_path):
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)


def get_random_routes(file_path):
    rm = RandomMap(file_path)
    rm.init_routes()
    rm.populate_routes_linehauls()
    rm.populate_routes_backhauls()
    rm.calculate_cost()
    rnd_maps_list.append(rm)


def get_a1_rm():
    local_search("Instances/A1.txt")


def get_all_rm():
    instances = sorted(glob.glob("Instances/*.txt"))
    map(lambda instance: local_search(instance), instances)


def local_search(path):
    ls = LocalSearchManager()
    ls1 = LocalSearchManager()
    ls.get_random_routes(path)
    ls1.get_random_routes(path)

    print '>> ', ls.file_name
    name = ls.file_name.split(".")[0]

    ensure_dir("Results/" + name + "/")
    payload = {'map': None,
               'cost': 0.0,
               'gap': 0.0,
               'maxload': 0.0,
               'num_clients': 0.0}
    map, cost, gap, num_clients = ls.execute('best_relocate')
    assert isinstance(map, RandomMap)

    payload['map'] = map
    payload['cost'] = cost
    payload['maxload'] = map.get_routes[0].get_nodes[0].get_capacity
    payload['gap'] = gap
    payload['num_clients'] = num_clients
    all_routes = map.get_routes
    fw = FileWriter("Results/" + name + "/best_relocate.txt")
    write_problem_details(fw, payload)
    write_solution_details(fw, payload)
    write_all_routes(fw, all_routes)
    print '-----------'
    map, cost, gap, num_clients = ls.execute('first_relocate')
    payload['map'] = map
    payload['cost'] = cost
    payload['maxload'] = map.get_routes[0].get_nodes[0].get_capacity
    payload['gap'] = gap
    payload['num_clients'] = num_clients
    all_routes = map.get_routes
    fw = FileWriter("Results/" + name + "/first_relocate.txt")
    write_problem_details(fw, payload)
    write_solution_details(fw, payload)
    write_all_routes(fw, all_routes)
    print '-----------'
    map, cost, gap, num_clients = ls1.execute('best_exchange')
    payload['map'] = map
    payload['cost'] = cost
    payload['maxload'] = map.get_routes[0].get_nodes[0].get_capacity
    payload['gap'] = gap
    payload['num_clients'] = num_clients
    all_routes = map.get_routes
    fw = FileWriter("Results/" + name + "/best_exchange.txt")
    write_problem_details(fw, payload)
    write_solution_details(fw, payload)
    write_all_routes(fw, all_routes)
    print '-----------'
    map, cost, gap, num_clients = ls1.execute('first_exchange')
    payload['map'] = map
    payload['cost'] = cost
    payload['maxload'] = map.get_routes[0].get_nodes[0].get_capacity
    payload['gap'] = gap
    payload['num_clients'] = num_clients
    all_routes = map.get_routes
    fw = FileWriter("Results/" + name + "/first_exchange.txt")
    write_problem_details(fw, payload)
    write_solution_details(fw, payload)
    write_all_routes(fw, all_routes)


def write_problem_details(writer, payload):
    writer.write("PROBLEM DETAILS:")
    writer.write("\nCustomers = " + str(payload['num_clients']))
    writer.write("\nMax Load = " + str(payload['maxload']))
    writer.write("\nMax Cost = 99999999999999")


def write_solution_details(writer, payload):
    # write solution details to file
    writer.write("\n\nSOLUTION DETAILS: ")
    writer.write("\nTotal Cost = " + str(payload['cost']))
    writer.write("\nRoutes Of the Solution = " + str(len(payload['map'].get_routes)))
    writer.write("\nGAP = " + str(payload['gap']) + " %")


def write_all_routes(writer, all_routes):
    # write all routes to file
    for route in all_routes:
        assert isinstance(route, Route)
        writer.write("\n\nROUTE " + str(route.get_index) + ":")
        writer.write("\nCost = " + str(route.get_cost))
        writer.write("\nDelivery Load = " + str(route.get_delivery_load))
        writer.write("\nPick-Up Load = " + str(route.get_pickup_load))
        writer.write("\nCustomers in Route = " + str(len(route.get_nodes)))
        # writer.write("\nVertex Sequence :\n" + route["vertices"])


def main():
    get_a1_rm()
    # get_all_rm()
    # local_search()


if __name__ == '__main__':
    main()
