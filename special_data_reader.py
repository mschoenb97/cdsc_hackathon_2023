""" Data Reading utilities """

import os

import pandas as pd

def read_data(file_path):
    """
    Read data into pandas dataframe

    :param file_path: str
        string filename
    :return: pd.DataFrame
    """

    basename = os.path.basename(file_path)

    if basename == 'wishes.csv':
        return _read_wishes_data(file_path)

    return pd.read_csv(file_path)


def _read_wishes_data(file_path):

    with open(file_path, 'r') as f:
        data = f.readlines()

    res = []

    in_list = False
    current_list = []

    columns = data[0].replace('"', '').replace('\n', '').split(',')

    for line in data[1:]:
        parsed_line = []
        for elt in line.replace('\n', '').split(','):
            if elt[0] != '{' and not in_list:
                parsed_line.append(elt)
            elif in_list:
                current_list.append(elt.split('}')[0])
            else:
                in_list = True
                current_list.append(elt.split('{')[1])

            if in_list and elt.endswith('}'):
                in_list = False
                parsed_line.append(current_list)
                current_list = []

        # assert len(parsed_line) == len(columns), (len(parsed_line), len(columns))
        if not len(parsed_line) == len(columns):
            import pdb; pdb.set_trace()
        res.append(parsed_line)

    return pd.DataFrame(res, columns=columns)