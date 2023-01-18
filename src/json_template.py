
import json
from string import Template
from typing import Any, Dict, Union, List, Mapping, Callable

JsonValue = Union[str, List['JsonValue'], Dict[str, 'JsonValue']]
JsonDict = Union[List[JsonValue], Dict[str, JsonValue]]
StrMapping = Mapping[str, Any]


def load_template(template_file: str) -> Callable[[StrMapping], JsonDict]:
    with open(template_file) as f:
        t = Template(f.read())
    return lambda mapping: json.loads(t.safe_substitute(quote_values(mapping)))


def load_json(template_file: str, mapping: StrMapping) -> JsonDict:
    return load_template(template_file)(mapping)


def quote_values(mapping: StrMapping) -> Dict[str, str]:
    def convert(x):
        if isinstance(x, (list, dict)):
            return json.dumps(x)
        return f'"{x}"'

    return {k: convert(v) for k, v in mapping.items()}


if __name__ == '__main__':
    json_loader = load_template('template/template.json')

    params = {
        'int': 1,
        'str': '文字列',
        'dict': {'key': '値', 'list': [3, 4, 5]},
        'list': [1, 2, 3, {'key': 'value'}]
    }

    j = json_loader(params)
    print(j)
    print(json.dumps(j, ensure_ascii=False))
