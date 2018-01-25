import glob

from business.LocalSearchManager import LocalSearchManager
from business.RandomMap import RandomMap

rnd_maps_list = []


def get_random_routes(file_path):
    rm = RandomMap(file_path)
    rm.init_routes()
    rm.populate_routes_linehauls()
    rm.populate_routes_backhauls()
    rm.calculate_cost()
    rnd_maps_list.append(rm)


def get_a1_rm():
    local_search("Instances/A1.txt")
    print rnd_maps_list


def get_all_rm():
    instances = sorted(glob.glob("Instances/*.txt"))
    map(lambda instance: local_search(instance), instances)
    print rnd_maps_list


def local_search(path):
    ls = LocalSearchManager()
    ls.get_random_routes(path)
    print '>> ', ls.file_name
    ls.execute('best_exchange')
    print '__________________________'
    ls.execute('first_exchange')


def main():
    get_a1_rm()
    # get_all_rm()
    # local_search()


if __name__ == '__main__':
    main()
