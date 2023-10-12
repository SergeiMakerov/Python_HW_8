# Ваша задача - написать программу, которая принимает на вход директорию и рекурсивно обходит эту директорию и все вложенные директории. Результаты обхода должны быть сохранены в нескольких форматах: JSON, CSV и Pickle. Каждый результат должен содержать следующую информацию:
# Путь к файлу или директории: Абсолютный путь к файлу или директории. Тип объекта: Это файл или директория. Размер: Для файлов - размер в байтах, для директорий - размер, учитывая все вложенные файлы и директории в байтах. Важные детали:
# Для дочерних объектов (как файлов, так и директорий) укажите родительскую директорию.
# Для файлов сохраните их размер в байтах.
# Для директорий, помимо их размера, учтите размер всех файлов и директорий, находящихся внутри данной директории, и вложенных директорий.
# Программа должна использовать рекурсивный обход директорий, чтобы учесть все вложенные объекты.
# Результаты должны быть сохранены в трех форматах: JSON, CSV и Pickle. Форматы файлов должны быть выбираемыми.
# Для обхода файловой системы вы можете использовать модуль os.
# Вам необходимо написать функцию traverse_directory(directory), которая будет выполнять обход директории и возвращать результаты в виде списка словарей. После этого результаты должны быть сохранены в трех различных файлах (JSON, CSV и Pickle) с помощью функций save_results_to_json, save_results_to_csv и save_results_to_pickle.

import json
import csv
import pickle
import os
from pathlib import Path


def save_results_to_json(data_dict: dict, path: str, file_name: str) -> None:                             #запись словаря в json файл
    file_path = os.path.join(path, file_name + '.json')
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data_dict, f, indent=4)


def save_results_to_csv(data_dict: dict, path: str, file_name: str) -> None:                             #запись словаря в csv файл
    file_path = os.path.join(path, file_name + '.csv')
    data = [['Path', 'object_type',  'object_name', 'object_size', 'parant_directory']]
    for key, value in data_dict.items():
        data.append([key, *value.values()])
    print(data)

    with open(file_path, 'w', encoding='utf-8') as f:
        write_csv = csv.writer(f, dialect='excel', delimiter=' ')
        write_csv.writerows(data)


def save_results_to_pickle(data_dict: dict, path: str, file_name: str) -> None:                                #запись словаря в pickle файл
    file_path = os.path.join(path, file_name + '.pickle')
    with open(file_path, 'wb') as f:
        pickle.dump(data_dict, f)


def dct_formatter1(total_dct: dict[str, dict[str]], path: str, item_name: str, item_type: str) -> None:
    if item_type == 'F':
        total_dct[path] = dict(object_type='File',
                               object_name=item_name,
                               object_size=os.path.getsize(os.path.join(path, item_name)),
                               parant_directory=os.path.split(path)[-1])
    elif item_type == 'D':
        total_dct[path] = dict(object_type='Directory',
                               object_name=item_name,
                               object_size=count_size(os.path.join(path, item_name)),
                               parant_directory=os.path.split(os.path.abspath(path))[-1])
    else:
        pass


def count_size(count_path: str, dir_size: int = 0) -> float:
    for sub_item in os.walk(count_path):

        if sub_item[2]:
            dir_size += sum([os.path.getsize(os.path.join(sub_item[0], file))for file in sub_item[2]])  # размер всех файлов в директории

        if sub_item[1]:
            dir_size += sum([count_size(os.path.join(sub_item[0], subdir))for subdir in sub_item[1]])

    return dir_size


def dir_walker(aim_path: str, total_dct: dict = None) -> dict[str, dict[str]]:
    if total_dct is None:
        total_dct = {}
        basic_path = os.path.split(os.path.abspath(aim_path))                                           

        dct_formatter1(total_dct, os.path.join(*basic_path[:-1]), basic_path[-1], 'D')


    for item in os.listdir(aim_path):
        check_path = os.path.join(aim_path, item)
        if os.path.isfile(check_path):
            dct_formatter1(total_dct, aim_path, item, 'F')
        elif os.path.isdir(check_path):
            dct_formatter1(total_dct, aim_path, item, 'D')
            dir_walker(os.path.join(aim_path, item), total_dct)
    return total_dct


# def dict_printer(in_dict: dict) -> None:
#     for i_key, i_val in sorted(in_dict.items()):
#         print(i_key, end=':')
#         if isinstance(i_val, dict):
#             print()
#             dict_printer(i_val)
#         else:
#             print('\t', i_val)


def main():

    tst_path = str(Path.cwd()) + '\\'
    #tst_path = ''

    result = dir_walker(tst_path)
    save_results_to_json(result, os.getcwd(), 'result1')
    save_results_to_pickle(result, os.getcwd(), 'result1')
    save_results_to_csv(result, os.getcwd(), 'result1')
    #dict_printer(result)


if __name__ == '__main__':
    main()