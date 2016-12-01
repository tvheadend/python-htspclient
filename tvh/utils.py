def getindex(obj, dotted_path, split_by='.'):
    """
    input dict

    d = {'a': {'cnt': 1}}
    getindex(d, 'a.cnt')
    returns 1

    :param obj:
    :param dotted_path:
    :param split_by:
    :return:
    """
    keys = dotted_path.split(split_by)
    tmp = obj
    for k in keys:
        if k.isdigit():
            k = int(k)
        tmp = tmp[k]
    return tmp
