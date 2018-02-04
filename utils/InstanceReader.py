import sys



class InstanceReader:
    def __init__(self, path):
        try:
            self._file = open(path, "r")
            self._path = path
            self._lines = self._file.readlines()
            self._lines = [x.rstrip() for x in self._lines]
            self._file.close()
        except IndexError:
            print("Error - Please specify an input file.")
            sys.exit(2)

    def get_nodes(self):
        nodes = []
        for i in range(3, len(self._lines)):
            nodes.append(self._lines[i])
        return nodes

    def get_clients_count(self):
        return self._lines[0]

    def get_stock(self):
        return self._lines[1]

    def get_routes_count(self):
        return self._lines[2]

    def get_deposit(self):
        return self._lines[3]

    def get_max_capacity(self):
        return self.get_deposit().split('   ')[3]

    def get_file_name(self):
        path = self._path.split("/")
        return path[-1]

    def get_node_by_index(self, idx):
        return self._lines[int(idx) + 3]
