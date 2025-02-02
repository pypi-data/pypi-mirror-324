from collections import OrderedDict
from sendero import get, list_paths


def flatten(
    data,
    columns=None,
    start=".",
    clean=False,
    offset=0,
    limit=None,
    skip_empty_columns=False,
    delimiter=".",
    sort=False,
    subdelimiter=";",
    stringify=True,
    unique=False,
):
    items = data if start in [".", "", "None"] else get(data, start)

    if not isinstance(items, list):
        raise Exception("[flatmate] invalid items")

    if not columns:
        columns = OrderedDict(
            [(path, path) for path in list_paths(data) if path.startswith(start)]
        )
    else:
        columns = OrderedDict(columns)

    rows = []
    imax = offset + (min(limit, len(items)) if str(limit).isdigit() else len(items))
    for item in items[:imax]:
        row = {}
        for colname, colpath in columns.items():
            colpath = colpath.lstrip(".")

            # remove start from colpath
            if colpath.startswith(start):
                colpath = colpath[len(start) :]

            got = get(
                item,
                colpath,
                clean=clean,
                delimiter=delimiter,
                sort=sort,
                stringify=stringify,
                unique=unique,
            )
            if stringify:
                row[colname] = subdelimiter.join(got)
            elif len(got) == 0:
                row[colname] = None
            elif len(got) == 1:
                row[colname] = got[0]
            elif len(got) > 1 and all([isinstance(it, str) for it in got]):
                row[colname] = got
            else:
                row[colname] = got

        rows.append(row)

    if skip_empty_columns:
        # start out assuming all columns are empty before reading first row
        empty_columns = columns
        for row in rows:
            # only keep if continue not to find valid values
            empty_columns = [
                col
                for col in columns
                if row[col] in [None, "", "null", "undefined", "none", "None"]
            ]

        if len(empty_columns) >= 1:
            for row in rows:
                for col in empty_columns:
                    del row[col]

    return rows
