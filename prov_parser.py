import entity_parser
import json

f = open("sample.provn", "r")
lines = f.readlines()

nodes = []
edges = []


def parseLine(line):
    parsed_line = line.partition("(")

    for x in parsed_line:
        x = x.strip()

    keyword = parsed_line[0].strip()

    match keyword:
        case "entity":
            print("found an entity.")
            nodes.append(
                entity_parser.parseSimpleEvent(parsed_line[2], "entity")
            )  # remove o inicio do paranteses mas o fim continua

        case "activity":
            print("found an activity.")
            nodes.append(
                entity_parser.parseActivity(parsed_line[2])
            )  # remove o inicio do paranteses mas o fim continua

        case "used":
            nodes.append(entity_parser.parseUsed(parsed_line[2], nodes, edges))

        case "agent":
            nodes.append(entity_parser.parseSimpleEvent(parsed_line[2], "agent"))

        case "wasGeneratedBy":
            entity_parser.parseWasGeneratedBy(parsed_line[2], nodes, edges)

        case "wasAssociatedWith":
            entity_parser.parseWasAssociatedWith(parsed_line[2], nodes, edges)

        case "wasInformedBy":
            entity_parser.parseWasInformedBy(parsed_line[2], nodes, edges)
    # print(nodes)


for line in lines:
    line = line.replace("\n", "")
    parseLine(line)
    # print(line)


with open(r"nodes.json", "w") as fp:
    fp.write("[")
    for item in nodes:
        # write each item on a new line
        fp.write("%s" % item)
        fp.write(",\n")
    fp.write("]")
    print("Done")
    fp.close()

with open(r"edges.json", "w") as f2:
    f2.write("[")
    for item in edges:
        # write each item on a new line
        f2.write("%s" % item)
        f2.write(",\n")
    f2.write("]")
    print("Done")
    f2.close()
