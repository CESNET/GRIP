def create_node(idea):
    req = 'Format: "IDEA0"'
    for key in idea:
        if key not in ['ID', 'DetectTime', 'Description', 'Category']:
            continue
        if key == 'Format':
            continue
        if isinstance(idea[key], list):
            if isinstance(idea[key][0], dict):
                for key2 in idea[key][0]:
                    if isinstance(idea[key][0][key2], list):
                        req += ', ' + key + '_' + key2 + ': ' + str(idea[key][0][key2]) + ''
                    else:
                        req += ', ' + key + '_' + key2 + ': "' + str(idea[key][0][key2]) + '"'
            else:
                req += ', ' + key + ': ' + str(idea[key]) + ''
        else:
            req += ', ' + key + ': "' + str(idea[key]) + '"'
    print(req)
    return req
