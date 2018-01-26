import glob
import os

from business.LocalSearchManager import LocalSearchManager
from business.RandomMap import RandomMap
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
    local_search("Instances/A2.txt")


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

    br = ls.execute('best_relocate')
    print '-----------'
    fr = ls.execute('first_relocate')
    print '-----------'
    be = ls1.execute('best_exchange')
    print '-----------'
    fe = ls1.execute('first_exchange')

    fw = FileWriter("Results/" + name + "/first_relocate.txt")
    fw.write(str(fr))
    fw = FileWriter("Results/" + name + "/best_relocate.txt")
    fw.write(str(br))

    fw = FileWriter("Results/" + name + "/first_exchange.txt")
    fw.write(str(fe))
    fw = FileWriter("Results/" + name + "/best_exchange.txt")
    fw.write(str(be))


def main():
    get_a1_rm()
    # get_all_rm()
    # local_search()


if __name__ == '__main__':
    main()
