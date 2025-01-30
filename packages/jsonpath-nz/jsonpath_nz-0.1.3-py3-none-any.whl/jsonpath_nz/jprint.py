import json
def jprint(data, load=False, marshall=True, indent=2):
    """
    Print formatted data
    
    Args:
        data (str): Data to print
        load (bool): Whether to load JSON data
        marshall (bool): Whether to marshal JSON data
        indent (int): Indentation level for JSON output
    """
    def _stringify_val(data):
        if isinstance(data, dict):
            return {k: _stringify_val(v) for k, v in data.items()}
        elif isinstance(data, list):
            return [_stringify_val(v) for v in data]
        elif isinstance(data, (str, int, float)):
            return data
        return str(data)

    _data = _stringify_val(data) if marshall else data
    try:
        _d = (
            json.dumps(json.loads(_data), indent=indent) if load else
            json.dumps(_data, indent=indent)
        )
    except:
        _d = _data

    print(_d)

