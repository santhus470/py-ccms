import os.path
from helper import consts
import json


def get_user_data_from_config_file():
    default_data_if_file_cant_acces = {
        "brightness": 1,
        "contrast": 1,
        "hvalue": 3,
        "const": 5,
        "block": 7,
        "twind": 7,
        "swind": 21

    }

    try:
        file_path = consts.json_dir
        with open(os.path.join(file_path, 'config.json'), 'w') as confg_file:
            print(file_path)
            data = json.load(confg_file)
            print('data', data)
            confg_file.close()
        return data
    except:
        return default_data_if_file_cant_acces


def get_thresh_input_data(read_values):
    block = read_values[consts.key_thresh_block]
    const = read_values[consts.key_thresh_const]
    t_win = read_values[consts.key_thresh_Templ_wind]
    s_win = read_values[consts.key_thresh_search_wind]
    h_value = read_values[consts.key_h_value]
    return block, const, t_win, s_win, h_value


def set_user_data_to_config_file(data):

    try:
        file_path = consts.json_dir
        confg_file = open(os.path.join(file_path, 'config.json'), 'r')
        json_data = json.load(confg_file)
        confg_file.close()
        json_data["hvalue"] = data[4]
        json_data["const"] = data[1]
        json_data["block"] = data[0]
        json_data["twind"] = data[2]
        json_data["swind"] = data[3]
        confg_file = open(os.path.join(file_path, 'config.json'), 'w')
        json.dump(json_data, confg_file)
        confg_file.close()
    except:
        pass
