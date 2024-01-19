def hasQuotes(parameter):
    if ":" in parameter:
        return True
    return False

def hasBracketOpening(parameter):
    if "[" in parameter:
        return True
    return False