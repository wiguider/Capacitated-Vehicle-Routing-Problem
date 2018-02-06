import csv
import glob
import json
import os
import sys
from multiprocessing import Process
from time import time

from business.LocalSearchManager import LocalSearchManager
from business.RandomMap import RandomMap
from models.Route import Route
from utils.FileWriter import FileWriter

sys.setrecursionlimit(10000)

rnd_maps_list = []

instances_map = [['Instances/A1.txt', 'Instances/A2.txt', 'Instances/A3.txt', 'Instances/A4.txt'],
                 ['Instances/B1.txt', 'Instances/B2.txt', 'Instances/B3.txt'],
                 ['Instances/C1.txt', 'Instances/C2.txt', 'Instances/C3.txt', 'Instances/C4.txt'],
                 ['Instances/D1.txt', 'Instances/D2.txt', 'Instances/D3.txt', 'Instances/D4.txt'],
                 ['Instances/E1.txt', 'Instances/E2.txt', 'Instances/E3.txt'],
                 ['Instances/F1.txt', 'Instances/F2.txt', 'Instances/F3.txt', 'Instances/F4.txt'],
                 ['Instances/G1.txt', 'Instances/G2.txt', 'Instances/G3.txt', 'Instances/G4.txt', 'Instances/G5.txt', 'Instances/G6.txt'],
                 ['Instances/H1.txt', 'Instances/H2.txt', 'Instances/H3.txt', 'Instances/H4.txt', 'Instances/H5.txt', 'Instances/H6.txt'],
                 ['Instances/I1.txt', 'Instances/I2.txt', 'Instances/I3.txt', 'Instances/I4.txt', 'Instances/I5.txt'],
                 ['Instances/J1.txt', 'Instances/J2.txt', 'Instances/J3.txt', 'Instances/J4.txt'],
                 ['Instances/K1.txt', 'Instances/K2.txt', 'Instances/K3.txt', 'Instances/K4.txt'],
                 ['Instances/L1.txt', 'Instances/L2.txt', 'Instances/L3.txt', 'Instances/L4.txt', 'Instances/L5.txt'],
                 ['Instances/M1.txt', 'Instances/M2.txt', 'Instances/M3.txt', 'Instances/M4.txt'],
                 ['Instances/N1.txt', 'Instances/N2.txt', 'Instances/N3.txt', 'Instances/N4.txt', 'Instances/N5.txt', 'Instances/N6.txt']]
first_relocate = {}
best_relocate = {}
first_exchange = {}
best_exchange = {}


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
    path = "Instances/G1.txt"
    local_search(path)


def get_all_rm():
    runInParallel(run_instances(0), run_instances(1), run_instances(2), run_instances(3), run_instances(4), run_instances(5), run_instances(6), run_instances(7), run_instances(7))


def run_instances(index):
    instances = instances_map[index]
    map(lambda instance: local_search(instance), instances)


def build_payload(map, cost, gap, num_clients):
    assert isinstance(map, RandomMap)
    payload = {'map': map, 'cost': cost, 'gap': float(gap), 'maxload': map.get_routes[0].get_nodes[0].get_capacity, 'num_clients': num_clients}
    return payload


def local_search(path):
    start_time = time()
    ls = LocalSearchManager(iterations=60)
    ls.get_random_routes(path)

    print '>> ', ls.file_name
    name = ls.file_name.split(".")[0]

    ensure_dir("Results/" + name + "/")

    run(ls, name)

    print 'Elapsed time: ' + str(round((time() - start_time) * 1000)) + ' ms'


def write_local_search_results(file_name, method, payload):
    try:
        all_routes = payload['map'].get_routes
        fw = FileWriter("Results/" + file_name + "/" + method + ".txt")
        write_problem_details(fw, payload)
        write_solution_details(fw, payload)
        write_all_routes(fw, all_routes)
        print '-----------'
    except Exception as e:
        print e


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


def write_results_to_json():
    files = sorted(glob.glob("Results/*/*.txt"))

    fd = {}
    for x in files:
        fn = x.split("/")[1]
        fd[fn] = []

    for fn in files:

        f = open(fn, "r")
        tt = fn.split("/")
        sol = open("RPA_Solutions/Detailed_Solution_" + tt[1] + ".txt")
        sol_lines = sol.readlines()
        lines = f.readlines()
        fd[tt[1]].append(
                {
                    "method": tt[2].split(".")[0],
                    "perfect_cost": sol_lines[8].split(" = ")[1].replace("\r\n", ""),
                    "our_cost": lines[6].split(" = ")[1].replace("\n", ""),
                    "gap": lines[8].split(" = ")[1].replace("%\n", "")}
        )
    res = "{"

    for key in sorted(fd.iterkeys()):
        res += "\"%s\": %s," % (key, fd[key])
    res += "}"

    res = res.replace("'", "\"")
    writer = FileWriter("res.json")
    writer.write(res)


def transform_json_to_csv():
    path = os.getcwd()
    inputfile = path + "/" + "res.json"
    outputfile = path + "/" + "res.csv"

    fieldheader = ["Instance", "BestKnown", "BestExchange", "GapBE", "BestRelocate", "GapBR", "FirstExchange", "GapFE", "FirstRelocate", "GapFR"]
    with open(inputfile, mode='r') as jsonfile, open(outputfile, mode="a") as csvfile:
        lines = json.load(jsonfile)
        csvwriter = csv.writer(csvfile, delimiter=',',
                               quotechar='|', quoting=csv.QUOTE_MINIMAL)
        csvwriter.writerow(fieldheader)
        for instance, methods in sorted(lines.iteritems()):
            tab = []
            perfeccost = -1
            for method in methods:
                gap = 0.0
                ourcost = 0.0
                for md, val in method.iteritems():
                    print md, val
                    if md == "perfect_cost":
                        perfeccost = float(val)
                    if md == "gap":
                        ourcost = ((float(str(val).replace(" %", "")) / 100) * perfeccost) + perfeccost
                        ourcost = round(ourcost, 2)
                        gap = val
                        tab.append(ourcost)
                        tab.append(gap)

            # writeHere
            tab0 = [instance, perfeccost]
            csvwriter.writerow(tab0 + tab)


def relocate(ls, name):
    try:
        print name
        map, cost, gap, num_clients = ls.execute('first_relocate')
        payload = build_payload(map, cost, gap, num_clients)
        write_local_search_results(name, 'first_relocate', payload)

        map, cost, gap, num_clients = ls.execute('best_relocate')
        payload = build_payload(map, cost, gap, num_clients)
        write_local_search_results(name, 'best_relocate', payload)
    except Exception as e:
        print e


def exchange(ls, name):
    print name
    map, cost, gap, num_clients = ls.execute('first_exchange')
    payload = build_payload(map, cost, gap, num_clients)
    write_local_search_results(name, 'first_exchange', payload)

    map, cost, gap, num_clients = ls.execute('best_exchange')
    payload = build_payload(map, cost, gap, num_clients)
    write_local_search_results(name, 'best_exchange', payload)


def run(ls, name):
    runInParallel(relocate(ls, name), exchange(ls, name))


def runInParallel(*fns):
    proc = []
    for fn in fns:
        p = Process(target=fn)
        p.start()
        proc.append(p)
    for p in proc:
        p.join()


def main():
    get_a1_rm()
    # get_all_rm()
    # local_search()
    # write_results_to_json()


if __name__ == '__main__':
    main()
