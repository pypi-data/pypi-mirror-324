def find_nodes(T, key_string, value_string):
    if isinstance(T, list):
        for x in T:
            for y in find_nodes(x, key_string, value_string):
                yield y
    if isinstance(T, dict):
        if key_string in T and T[key_string] == value_string:
            yield T

        else:
            for k in T:
                for x in find_nodes(T[k], key_string, value_string):
                    yield x

