import sys


class FileWriter:
    """Reads a file"""

    def __init__(self, path):
        try:

            self.file = open(path, "w+")

        except IndexError:
            print("Error - Please specify an input file.")
            sys.exit(2)

    def write(self, data):
        try:
            self.file.write(data)
        except Exception as e:
            print("Error - " + str(e.message))
            sys.exit(2)

    def close(self):
        self.file.close()
