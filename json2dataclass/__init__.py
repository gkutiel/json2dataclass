from dataclasses import dataclass
from typing import TextIO


@dataclass
class dclass:
    name: str
    props: list['prop']


@dataclass
class prop:
    name: str
    type: dclass | str


def json2dataclass(key: str, data):
    if isinstance(data, dict):
        return dclass(key, [prop(k, json2dataclass(k, v)) for k, v in data.items()])

    if isinstance(data, list):
        return 'list'

    if isinstance(data, str):
        return "str"

    if isinstance(data, int):
        return "int"

    if isinstance(data, float):
        return "float"

    assert False, f"Unknown type: {data}"


def dclass2py(node: dclass, out: TextIO):
    for prop in node.props:
        if isinstance(prop.type, dclass):
            dclass2py(prop.type, out)

    out.write('\n@dataclass\n')
    out.write(f"class {node.name}:\n")
    for prop in node.props:
        type = prop.type.name if isinstance(prop.type, dclass) else prop.type
        out.write(f'\t{prop.name}: {type}\n')


def cli(json_path: str, py_path: str, root_name: str = 'root'):
    import json

    with open(json_path) as f:
        data = json.load(f)

    res = json2dataclass(root_name, data)
    assert isinstance(res, dclass)

    with open(py_path, 'w') as f:
        dclass2py(res, f)


def main():
    from fire import Fire
    Fire(cli)


if __name__ == '__main__':
    import sys
    print()
    data = {"person": {"name": "John", "age": 30, "friends": []}}
    res = json2dataclass('main', data)

    assert isinstance(res, dclass)
    dclass2py(res, sys.stdout)
