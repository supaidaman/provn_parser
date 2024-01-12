f = open("sample.provn", "r")
lines = f.readlines()


edges = []

def parseLine(line):
    parsed_line = line.partition("(")
    keyword = parsed_line[0].strip()
    match keyword:
        case "entity":
            print("found an entity.")
            parseEntity(parsed_line[2]) # remove o inicio do paranteses mas o fim continua


def parseEntity(parameter_list):
    print("parameters")
    print(parameter_list)

for line in lines:
    line = line.replace("\n", "")
    parseLine(line)
    # print(line)

# {id:x, type: entity, label: "utk:grammar"}
# {id:y,type:agent,label, utk:autoAgent, parameters: [{x:y}]} //onde x = chave, y =valor
# {id:z,}

