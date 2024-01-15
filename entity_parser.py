import json

def parseEntity(parameters):
    print("parameters")
    parameters = parameters.replace(')','') #remove parenteses sobrando

    parsed_parameters = parameters.partition(",")
    parsed_parameters = list(filter(None, parsed_parameters))
    
    if(len(parsed_parameters) == 1):
        return json.dumps(
            {
                "id": parsed_parameters[0], 
                "type": "entity",
            }
        )
    else:
        return json.dumps(
            {
                "id": parsed_parameters[0], 
                "type": "entity",
                "optionalParameters": parsed_parameters[1]
            }
        )



def parseActivity(parameters):
    parameters = parameters.replace(')','') #remove parenteses sobrando

    parsed_parameters = parameters.partition(",")
    parsed_parameters = list(filter(None, parsed_parameters))

    if(len(parsed_parameters) == 1):
        return json.dumps(
            {
                "id": parsed_parameters[0], 
                "type": "activity",
            }
        )
    else:
        parameters_list = parsed_parameters[2].split(',')
        parameters_list = [s.strip() for s in parameters_list]

       
        if(len(parameters_list) > 2):
            optionalParameters = ' , '.join(parameters_list[2:])
            print(optionalParameters)
        else:
            optionalParameters = parsed_parameters[2]

    return json.dumps(
            {
                "id": parsed_parameters[0], 
                "type": "activity",
                "start_time": parameters_list[0],
                "end_time": parameters_list[1],
                "optionalParameters": optionalParameters,
            }
        )
#  activity(utk:save, 2024-01-06T12:30:05.238087, -, [prov:type="edit"])
# Here ex:a10 is the activity identifier,
# 2011-11-16T16:00:00 and 2011-11-16T16:00:01 are the optional start and end times for the activity, 
#and [prov:type="createFile"] is a list of optional attributes.