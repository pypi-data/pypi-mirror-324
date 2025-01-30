def matches_from_string(match_string: str):
    if ':' not in match_string:
            help_doc_string = """
            List of tags should be in the format of:
            "'ENVIRONMENT:UFGEnvironment:dev','ENVIRONMENT:AppGroup:guidewire_policycenter'" 
            It's a comma separated list of tags.
            Each tag is a colon separated list of context, key, value.
            Example: "'ENVIRONMENT:UFGEnvironment:dev','ENVIRONMENT:AppGroup:guidewire_policycenter'"
            Where colon separarted list is context, key, value.
            """
            print(help_doc_string)
            exit(code=1)    
    matches = []
    tags_list = []
    match_dict = {}
    parts = match_string.split(",")
    for part in parts:
        items = part.split(":")
        context = items[0]
        key = items[1]
        value = items[2]
        tag_dict = {"context": context, "key": key, "value": value}
        tags_list.append(tag_dict)
    match_dict["tags"] = tags_list
    match_dict["tagCombination"] = "AND"
    match_dict["type"] = None
    match_dict["mzId"] = None
    match_dict["managementZoneId"] = None
    matches.append(match_dict)
    return matches


def scope_from_lists(entities: list, matches: list):
    scope_dict = {"entities": entities, "matches": matches}
    return scope_dict


if __name__ == "__main__":
    print("This is a library")
