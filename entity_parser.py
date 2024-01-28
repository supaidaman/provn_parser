import json
import uuid
import dateparser

from parameter_type_checker import hasBracketOpening, hasQuotes, hasSubString


class Object:
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True)


def parseActivity(parameters):
    parameters = parameters.replace(")", "")  # remove parenteses sobrando

    parsed_parameters = parameters.partition(",")
    parsed_parameters = list(filter(None, parsed_parameters))

    if len(parsed_parameters) == 1:
        return json.dumps(
            {
                "data": {
                    "id": parsed_parameters[0],
                    "type": "activity",
                }
            }
        )
    else:
        parameters_list = parsed_parameters[2].split(",")
        parameters_list = [s.strip() for s in parameters_list]

        if len(parameters_list) > 2:
            optionalParameters = " , ".join(parameters_list[2:])
            print(optionalParameters)
        else:
            optionalParameters = parsed_parameters[2]

    return json.dumps(
        {
            "data": {
                "id": parsed_parameters[0],
                "type": "activity",
                "start_time": parameters_list[0],
                "end_time": parameters_list[1],
                "optionalParameters": optionalParameters,
            }
        }
    )


# TODO -> IDENTIFY TYPE OF PARAMETER TO ENTER THE SPECIFIC FIELDS OF JSON
# NÃO TEM CAMPO, USA - no json.
# TEM -, ignora
# activity(ex:a10)
# activity(ex:a10, -, -)
# activity(ex:a10, -, -, [prov:type="edit"])
# activity(ex:a10, -, 2011-11-16T16:00:00)
# activity(ex:a10, 2011-11-16T16:00:00, -)
# activity(ex:a10, 2011-11-16T16:00:00, -, [prov:type="createFile"])
# activity(ex:a10, [prov:type="edit"])


# parser para eventos que só tem id e lista de parametros opcionais
def parseSimpleEvent(parameters, event_type):
    parameters = parameters.replace(")", "")  # remove parenteses sobrando

    parsed_parameters = parameters.partition(",")
    parsed_parameters = list(filter(None, parsed_parameters))

    if len(parsed_parameters) == 1:
        return json.dumps(
            {
                "data": {
                    "id": parsed_parameters[0],
                    "type": event_type,
                }
            }
        )
    return json.dumps(
        {
            "data": {
                "id": parsed_parameters[0],
                "type": event_type,
                "optionalParameters": parsed_parameters[2],
            }
        }
    )


def parseWasGeneratedBy(parameters, nodes, edges):
    parameters = parameters.replace(")", "")  # remove parenteses sobrando

    parsed_parameters = parameters.split(",")
    parameters_list = list(filter(None, parsed_parameters))
    parameters_list = [s.strip() for s in parameters_list]

    wasGeneratedBy = Object()
    wasGeneratedBy.type = "wasGeneratedBy"

    for idx, p in enumerate(parameters_list):
        if idx == 0:
            if hasQuotes(p) and hasSubString(p, ";"):
                wasGeneratedBy.identifier = p
            else:
                wasGeneratedBy.entity = p
                wasGeneratedBy.id = p
            continue

        if idx >= 0 and not hasattr(wasGeneratedBy, "entity"):
            wasGeneratedBy.entity = p
            wasGeneratedBy.id = p
            continue

        if idx >= 1 and not hasattr(wasGeneratedBy, "activity"):
            wasGeneratedBy.activity = p
            continue

        if idx >= 1 and dateparser.parse(p):
            wasGeneratedBy.start_time = p
            continue

        if idx >= 1 and hasBracketOpening(p):
            optionalParameters = " , ".join(parameters_list[idx:])
            wasGeneratedBy.optionalParameters = optionalParameters
            break
            # sempre é o último parametro

    # if not hasattr(wasGeneratedBy, "activity"):  # todo get prefix to attributes
    #     wasGeneratedBy.id = uuid.uuid4()
    # activity indica relação!

    jsondata = {}
    jsondata["data"] = wasGeneratedBy.__dict__
    nodes.append(json.dumps(jsondata))

    edges.append(
        json.dumps(
            {
                "data": {
                    "target": wasGeneratedBy.activity,
                    "source": wasGeneratedBy.id,
                }
            }
        )
    )
    return


# wasGeneratedBy(e2, a1, 2011-11-16T16:00:00)
# wasGeneratedBy(e2, a1, -, [ex:fct="save"])
# wasGeneratedBy(e2, [ex:fct="save"])
# wasGeneratedBy(ex:g1; e)
# wasGeneratedBy(ex:g1; e, a, tr:WD-prov-dm-20111215)


def parseWasAssociatedWith(parameters, nodes, edges):
    parameters = parameters.replace(")", "")  # remove parenteses sobrando

    parsed_parameters = parameters.split(",")
    parameters_list = list(filter(None, parsed_parameters))
    parameters_list = [s.strip() for s in parameters_list]

    wasAssociatedWith = Object()
    wasAssociatedWith.type = "wasAssociatedWith"

    for idx, p in enumerate(parameters_list):
        if idx == 0:
            if hasQuotes(p) and hasSubString(p, ";"):
                wasAssociatedWith.identifier = p
            else:
                wasAssociatedWith.activity = p
            continue

        if idx == 1 and not hasattr(wasAssociatedWith, "activity"):
            wasAssociatedWith.activity = p
            continue

        if idx >= 1 and not hasattr(wasAssociatedWith, "agent"):
            wasAssociatedWith.agent = p
            wasAssociatedWith.id = p
            continue

        if idx >= 1 and not hasattr(wasAssociatedWith, "plan"):
            wasAssociatedWith.plan = p
            continue

        if idx > 0 and hasBracketOpening(p):
            optionalParameters = " , ".join(parameters_list[idx:])
            print(optionalParameters)
            wasAssociatedWith.optionalParameters = optionalParameters
            break
            # sempre é o último parametro

    if not hasattr(wasAssociatedWith, "agent"):  # todo get prefix to attributes
        wasAssociatedWith.agent = p
        wasAssociatedWith.id = uuid.uuid4()

    if not hasattr(wasAssociatedWith, "agent"):  # todo get prefix to attributes
        wasAssociatedWith.agent = uuid.uuid4()

    # activity indica relação!
    jsondata = {}
    jsondata["data"] = wasAssociatedWith.__dict__
    nodes.append(json.dumps(jsondata))

    edges.append(
        json.dumps(
            {
                "data": {
                    "target": wasAssociatedWith.id,
                    "source": wasAssociatedWith.activity,
                    "type": "wasAssociatedWith"
                }
            }
        )
    )
    return


# wasAssociatedWith(ex:assoc; ex:a1, ex:ag1, ex:e1, [ex:param1="a", ex:param2="b"])
# wasAssociatedWith(ex:a1, -, ex:e1)
# wasAssociatedWith(ex:a1, ex:ag1)
# wasAssociatedWith(ex:a1, ex:ag1, ex:e1)
# wasAssociatedWith(ex:a1, ex:ag1, ex:e1, [ex:param1="a", ex:param2="b"])
# wasAssociatedWith(ex:assoc; ex:a1, -, ex:e1)


def parseUsed(parameters, nodes, edges):
    parameters = parameters.replace(")", "")  # remove parenteses sobrando

    parsed_parameters = parameters.split(",")
    parameters_list = list(filter(None, parsed_parameters))
    parameters_list = [s.strip() for s in parameters_list]

    used = Object()
    used.type = "used"

    for idx, p in enumerate(parameters_list):
        if idx == 0:
            if hasQuotes(p) and hasSubString(p, ";"):
                used.identifier = p
                used.id = p
            else:
                used.activity = p
            continue

        if idx == 1 and not hasattr(used, "activity"):
            used.activity = p
            continue

        if idx >= 1 and not hasattr(used, "entity"):
            used.entity = p

            continue

        if idx >= 1 and dateparser.parse(p):
            used.start_time = p
            continue

        if idx > 0 and hasBracketOpening(p):
            optionalParameters = " , ".join(parameters_list[idx:])
            print(optionalParameters)
            used.optionalParameters = optionalParameters
            break
            # sempre é o último parametro

    if not hasattr(used, "id"):  # todo get prefix to attributes
        used.id = uuid.uuid4()

    # activity indica relação!
    # relação somente de edge
    edges.append(
        json.dumps(
            {
                "data": {
                    "target": used.entity,
                    "source": used.activity,
                    "type": "used"
                }
            }
        )
    )
    return


# used(ex:act2)
# used(ex:act2, ar3:0111, 2011-11-16T16:00:00)
# used(a1,e1, -, [ex:fct="load"])
# used(ex:u1; ex:act2, ar3:0111, -)
def parseUsed(parameters, nodes, edges):
    parameters = parameters.replace(")", "")  # remove parenteses sobrando

    parsed_parameters = parameters.split(",")
    parameters_list = list(filter(None, parsed_parameters))
    parameters_list = [s.strip() for s in parameters_list]

    wasInformedBy = Object()
    wasInformedBy.type = "used"

    for idx, p in enumerate(parameters_list):
        if idx == 0:
            if hasQuotes(p) and hasSubString(p, ";"):
                wasInformedBy.identifier = p
                wasInformedBy.id = p
            else:
                wasInformedBy.informed_activity = p
            continue

        if idx == 1 and not hasattr(wasInformedBy, "informed_activity"):
            wasInformedBy.informed_activity = p
            continue

        if idx >= 1 and not hasattr(wasInformedBy, "informant_activity"):
            wasInformedBy.informant_activity = p

            continue

        if idx > 0 and hasBracketOpening(p):
            optionalParameters = " , ".join(parameters_list[idx:])
            print(optionalParameters)
            wasInformedBy.optionalParameters = optionalParameters
            break
            # sempre é o último parametro

    if not hasattr(wasInformedBy, "id"):  # todo get prefix to attributes
        wasInformedBy.id = uuid.uuid4()

    # relação somente de edge
    edges.append(
        json.dumps(
            {
                "data": {
                    "target": wasInformedBy.informed_activity,
                    "source": wasInformedBy.informant_activity,
                    "type": "wasInformedBy"
                }
            }
        )
    )
    return

# wasInformedBy(ex:a1, ex:a2)
# wasInformedBy(ex:a1, ex:a2, [ex:param1="a", ex:param2="b"])
# wasInformedBy(ex:i; ex:a1, ex:a2)
# wasInformedBy(ex:i; ex:a1, ex:a2, [ex:param1="a", ex:param2="b"])