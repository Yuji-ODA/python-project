
import json
from string import Template
from typing import Dict, Union, List, Mapping, Callable

JsonType = Union[str, int, float, List['JsonType'], Dict[str, 'JsonType']]
JsonMapping = Mapping[str, JsonType]


def load_template(template_file: str) -> Callable[[JsonMapping], JsonType]:
    with open(template_file) as f:
        t = Template(f.read())
    return lambda mapping: json.loads(t.safe_substitute({k: json.dumps(v) for k, v in mapping.items()}))


def load_json(template_file: str, mapping: JsonMapping) -> JsonType:
    return load_template(template_file)(mapping)


if __name__ == '__main__':
    json_loader = load_template('template/template.json')

    params = {
        'int': 1.2,
        'str': '文字列',
        'dict': {'key': '値', 'list': [3, 4, 5]},
        'list': [1, 2, 3, {'key': 'value'}],
    }

    print(json_loader(params))
