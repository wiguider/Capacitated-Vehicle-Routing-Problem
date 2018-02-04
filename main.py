import csv
import json
import os


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


if __name__ == '__main__':
    transform_json_to_csv()
