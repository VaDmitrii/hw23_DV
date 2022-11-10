import os
from json import JSONDecodeError
from typing import Generator

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")


def load_data(file_name: str) -> Generator:
    try:
        with open(f'{DATA_DIR}/{file_name}', 'r', encoding='utf-8') as file:
            for row in file:
                yield row
    except (FileNotFoundError, JSONDecodeError):
        return 'No such file in directory', 400


def filter_data(data, value):
    return filter(lambda l: value in l, data)


def map_data(data, value):
    value = int(value)
    return map(lambda l: l.split(' ')[value], data)


def limit_result(data, limit_value):
    limit_value = int(limit_value)
    return list(data)[:limit_value]


def result_data(file_name: str, commands_dict: dict):
    result = load_data(file_name=file_name)
    if 'filter' in commands_dict.keys():
        result = filter_data(result, commands_dict['filter'])

    if 'map' in commands_dict.keys():
        result = map_data(result, commands_dict['map'])

    if 'sort' in commands_dict.keys():
        if commands_dict['sort'] == 'desc':
            result = sorted(result, reverse=True)
        else:
            result = sorted(result)

    if 'limit' in commands_dict.keys():
        result = limit_result(result, commands_dict['limit'])
    elif "unique" in commands_dict.keys():
        result = set(result)
    return result
