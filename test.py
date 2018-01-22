import glob

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
    get_random_routes("Instances/A1.txt")
    print rnd_maps_list


def get_all_rm():
    instances = sorted(glob.glob("Instances/*.txt"))
    map(lambda instance: get_random_routes(instance), instances)
    print rnd_maps_list


def main():
    get_a1_rm()
    # get_all_rm()


if __name__ == '__main__':
    main()
