# from rosidl_runtime_py import message_to_yaml


def get_field(data: object, fields: list[str]):
    for field in fields:
        data = getattr(data, field)
    return data


def set_field(data: object, fields: list[str], value: object):
    pass
