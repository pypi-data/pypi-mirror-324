import itertools


def flat_lists(ls):
    return [x for s in ls for x in s]


def split_list(ls, delimiter, include_delimiter):
    if not include_delimiter:
        spl = [
            list(y) for x, y in itertools.groupby(ls, lambda z: z == delimiter) if not x
        ]
    else:
        spl = []
        for x, y in itertools.groupby(ls, lambda z: z == delimiter):
            if x:
                spl.append([])
            spl[-1].extend(y)
    return spl
