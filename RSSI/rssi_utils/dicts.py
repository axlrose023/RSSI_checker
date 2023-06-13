def timeslots_less(data_list):
    lines = {}
    more = {}
    for data in data_list:
        for key, value in data.items():
            if isinstance(value, dict):
                for slot, val in value.items():
                    if 'timeslot1<timeslot2' in slot:
                        lines[key] = val
                    elif 'timeslot1>timeslot2' in slot:
                        more[key] = val
    return lines, more


def test_return():
    return "Side black line"


def return_dict(data):
    dicts = eval(data.data)
    for key in dicts:
        dicts[key] *= 3
    return dicts


def return_dict_erlang(data):
    dicts = eval(data.data)
    for key in dicts:
        if isinstance(dicts[key], int):
            dicts[key] /= 1200
            if dicts[key] == 0.0:
                dicts[key] = 0
    return dicts
