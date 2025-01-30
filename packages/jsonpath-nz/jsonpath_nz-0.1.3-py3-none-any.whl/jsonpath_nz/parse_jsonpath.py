import re


def parse_jsonpath(manifest, extend=None):
    """
    Parse a dictionary of JSONPath expressions to their corresponding names
    Args:
        manifest (dict): Dictionary with JSONPath expressions as keys and names as values
    Returns:
        dict: Processed JSONPath expressions
    """

    def check_jsonpath(expression):
        """Check the paranthese in json path"""
        open_tup = tuple("({[")
        close_tup = tuple(")}]")
        map = dict(zip(open_tup, close_tup))
        queue = []

        for i in expression:
            if i in open_tup:
                queue.append(map[i])
            elif i in close_tup:
                if not queue or i != queue.pop():
                    return "unbalanced"
        if not queue:
            return "balanced"
        else:
            return "unbalanced"

    def check_token(token):
        """Check given token is balanced"""
        open_quote = tuple("'\"")
        count = 0
        for i in token:
            if i in open_quote:
                count = count + 1
        if count % 2 == 0:
            return "balanced"
        else:
            return "unbalanced"

    def tokenize(tList):
        """Tokenize the list with valid balanced elements"""
        unbalanced = False
        try:
            i = 0
            while i < len(tList) - 1:
                if check_token(tList[i]) == "unbalanced":
                    unbalanced = True
                    eCount = 0
                    while unbalanced:
                        tList[i] = f"{tList[i]}.{tList.pop(i+1)}"
                        eCount = eCount + 1
                        if check_token(tList[i]) == "balanced":
                            break
                    i = i + eCount
                i = i + 1
            return tList
        except Exception as e:
            return [False, f"Error ({e}) field in xls {tList[i]}"]

    def split_string_with_array(string):
        arr = string.split("[")
        arr[1] = arr[1].replace("]", "")
        arr[1] = int(arr[1])
        return (arr[0], arr[1])

    def get_list(lsize, dict_value):
        """retrun the list based on size"""
        eDict = {}
        rList = []
        try:
            if not isinstance(lsize, int):
                return rList
            for i in range(lsize):
                rList.append(eDict)
            rList.append(dict_value)
            return rList
        except Exception as e:
            return rList

    def process_list(pList, key, value):
        """Process the list of json variables"""
        json_dict = tempDict = {}
        FKEY = key
        if len(pList) == 0:
            tempDict[key] = value
        else:
            key = pList.pop(0)
            if check_token(key) == "unbalanced":
                key = f"{key}.{pList.pop(0)}"
            tempDict[FKEY] = process_list(pList, key, value)
        return json_dict

    def process_subList(sDict):
        """Process the sub dictionary"""
        open_bracket = "["
        closed_bracket = "]"
        lDict = tDict = {}
        subList = []
        for k, v in sDict.items():
            if isinstance(v, dict):
                if (open_bracket in k) and (closed_bracket not in k):
                    k = re.findall(r"[0-9a-zA-Z=]+", k)[0]
                    subList.append(process_subList(v))
                    tDict[k] = subList

                strValues = re.findall(r"[0-9a-zA-Z=:._]+", k)
                if len(strValues) == 2:
                    if "==" in strValues[0]:
                        tDict[strValues[0].replace("==", "")] = strValues[1]
                        tDict.update(process_subList(v))
                if len(strValues) > 2:
                    if "==" in strValues[1]:
                        tDict[strValues[0]] = " ".join(strValues[2:])
                        # Its exception example "Texas A(6)" : Anything that has ( or ) in assigned value
                        ARValueList = tDict[strValues[0]].split(" ")
                        if ARValueList[0]:
                            ARValue = (
                                " ".join(ARValueList[:-1])
                                + "("
                                + ARValueList[-1]
                                + ")"
                            )
                            tDict[strValues[0]] = ARValue

                        tDict.update(process_subList(v))
            else:
                tDict.update({k: v})
        return lDict

    def process_dict(pDict):
        """Process the dictionary as given in json path"""
        open_bracket = "["
        closed_bracket = "]"
        json_dict = tempDict = {}
        subList = []

        for dict_key, dict_value in pDict.items():
            if not isinstance(dict_value, dict):
                tempDict[dict_key] = dict_value
            if (open_bracket in dict_key) and (closed_bracket in dict_key):
                dict_key, lsize = split_string_with_array(dict_key)
                if isinstance(dict_value, dict):
                    tempDict[dict_key] = get_list(lsize, process_dict(dict_value))
            elif (open_bracket in dict_key) and (closed_bracket not in dict_key):
                dict_key = re.findall(r"[0-9a-zA-Z=]+", dict_key)[0]
                subList.append(process_subList(dict_value))
                tempDict[dict_key] = subList
            else:
                if isinstance(dict_value, dict):
                    tempDict[dict_key] = process_dict(dict_value)
        return json_dict

    def merge_lists(aList, bList, path, extend=None):
        """Merge two lists"""

        def extendList(aList, bList, commonKey):
            """Extend list based on the given list"""
            bSet = set(bList[0].items())
            for i in range(0, len(aList)):
                aSet = set(aList[i].items())
                diffKey = set(dict((bSet.symmetric_difference(aSet))))
                if (len(diffKey.intersection(commonKey))) == 0:
                    aList[i] = dict(aSet.union(bSet))
                    bList = []
            aList.extend(bList)
            return aList

        a_emptyIdx = [idx for idx, s in enumerate(aList) if s == {}]
        b_emptyIdx = [idx for idx, s in enumerate(bList) if s == {}]

        pathList = list(path)
        if len(a_emptyIdx) == 0 and len(b_emptyIdx) == 0:
            if extend:
                for eKey, eValue in extend.items():
                    if isinstance(eValue, list):
                        if eKey in pathList:
                            for i in bList:
                                if len(i) > 1:
                                    return extendList(aList, bList, eValue)
                    else:
                        if eKey in pathList:
                            for i in bList:
                                if len(i) > 1:
                                    return extendList(aList, bList, eValue)

        cLen = min(len(aList), len(bList))

        for idx in range(cLen):
            if len(aList[idx]) == 0 and len(bList[idx]) != 0:
                aList[idx] = bList[idx]
            if isinstance(aList[idx], dict) and isinstance(bList[idx], dict):
                merge_dicts(aList[idx], bList[idx])
            elif isinstance(aList[idx], list) and isinstance(bList[idx], list):
                aList[idx].extend(bList[idx])
            else:
                aList[idx] = bList[idx]

        for idx in range(cLen, len(bList)):
            aList.append(bList[idx])

        return aList

    def merge_dicts(a, b, path=None, update=True, extend=None):
        """Merge 2 dictionaries"""
        if path is None:
            path = []

        if a == b:
            return a

        for key in b:
            if key in a:
                if isinstance(a[key], dict) and isinstance(b[key], dict):
                    merge_dicts(a[key], b[key], path + [str(key)], update, extend)
                elif a[key] == b[key]:
                    pass
                elif isinstance(a[key], list) and isinstance(b[key], list):
                    a[key] = merge_lists(a[key], b[key], path + [str(key)], extend)
                elif update:
                    a[key] = b[key]
                else:
                    raise Exception(f"Conflict at {'.'.join(path + [str(key)])}")
            else:
                a[key] = b[key]
        return a

    def jsonpath_to_dict(manifestItem):
        # Version 2.0
        jsonPath = manifestItem["json-path"]
        jsonValue = manifestItem["json-value"]

        if not jsonPath.startswith("$."):
            return {
                "error": f"Given JSON_PATH : {jsonPath}  is not starting with $.xxx"
            }

        if "unbalanced" == check_jsonpath(jsonPath):
            return {"error": f"Unbalanced JSON_PATH : {jsonPath}"}

        k_list = jsonPath.split(".")
        k_list = tokenize(k_list)
        if not k_list[0]:
            return {"error": f"Invalid JSONPATH [{jsonPath}({k_list[1]})]"}
        try:
            if k_list[0] == "$":
                k_list = k_list[1:]
                FKEY = k_list.pop(0)
                FVALUE = jsonValue
                plDict = process_list(k_list, FKEY, FVALUE)
                pdDict = process_dict(plDict)
                return pdDict
        except Exception as e:
            return {"error": f"Invalid JSONPATH: {jsonPath} ({e})"}

    tmp = {"data": []}
    for k, v in manifest.items():
        if "$" in k:
            if isinstance(v, str):
                if v.startswith('"'):
                    v = v[1:-1]
            tmp["data"].append({"json-path": k, "json-value": v})

    if not tmp["data"]:
        return {"error": "No data found in manifest"}

    json_payload = {}
    for item in tmp["data"]:
        genPayload = jsonpath_to_dict(item)
        if any("error" in k for k in genPayload):
            return genPayload
        json_payload = merge_dicts(json_payload, genPayload, update=True, extend=extend)
    return json_payload
