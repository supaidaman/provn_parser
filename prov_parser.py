from entity_parser import parseActivity, parseSimpleEvent
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
            nodes.append(parseSimpleEvent(parsed_line[2],"entity")) # remove o inicio do paranteses mas o fim continua

        case "activity":
            print("found an activity.")
            nodes.append(parseActivity(parsed_line[2])) # remove o inicio do paranteses mas o fim continua

        case "agent":
            nodes.append(parseSimpleEvent(parsed_line[2],"agent"))
    print(nodes)


for line in lines:
    line = line.replace("\n", "")
    parseLine(line)
    # print(line)

# {id:x, type: entity, label: "utk:grammar"}
# {id:y,type:agent,label, utk:autoAgent, parameters: [{x:y}]} //onde x = chave, y =valor
# {id:z,}

# entity(utk:grammar)
#   agent(utk:autoAgent, [prov:type="prov:SoftwareAgent", prov:type="ao:IBCCAlgo"])
#   activity(utk:save, 2024-01-06T12:30:05.238087, -, [prov:type="edit"])
#   wasGeneratedBy(utk:grammar, utk:save, -)
#   wasAssociatedWith(utk:save, utk:autoAgent, -, [prov:role="author"])
