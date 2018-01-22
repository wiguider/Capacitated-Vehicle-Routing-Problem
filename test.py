from business.RandomMap import RandomMap


def main():
    rm = RandomMap("Instances/A1.txt")
    rm.init_routes()
    rm.populate_routes_linehauls()
    rm.reset_routes_capacities()
    rm.populate_routes_backhauls()
    rm.calculate_cost()
    random_routes = rm.get_routes
    print random_routes
    print 'Total cost', rm.cost


if __name__ == '__main__':
    main()
