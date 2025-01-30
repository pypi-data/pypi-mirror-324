def parse_dict(data, parent_path="$", paths=None, extend=None):
    """
    Convert a dictionary to JSONPath expressions, handling both array indices and filter conditions
    """
    if paths is None:
        paths = {}

    if isinstance(data, dict):
        for key, value in data.items():
            current_path = f"{parent_path}.{key}"

            # Handle arrays that need filter conditions (specified in extend)
            if extend and key in extend and isinstance(value, list):
                filter_fields = extend[key]
                for item in value:
                    if not isinstance(item, dict):
                        continue

                    # Build filter conditions
                    conditions = []
                    target_field = None
                    target_value = None

                    for k, v in item.items():
                        if k in filter_fields:
                            conditions.append(f"@.{k} == '{v}'")
                        else:
                            target_field = k
                            target_value = v

                    if conditions and target_field:
                        filter_path = f"{current_path}[?({' && '.join(conditions)})].{target_field}"
                        paths[filter_path] = target_value

            # Handle regular arrays
            elif isinstance(value, list):
                for idx, item in enumerate(value):
                    if isinstance(item, dict):
                        for k, v in item.items():
                            array_path = f"{current_path}[{idx}].{k}"
                            paths[array_path] = v

            # Handle nested dictionaries
            elif isinstance(value, dict):
                parse_dict(value, current_path, paths, extend)

            # Handle simple key-value pairs
            else:
                paths[current_path] = value

    return paths
