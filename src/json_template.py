import json
from string import Template
from typing import Dict, Union, List, Mapping, Callable, Iterator

JsonValue = Union[str, int, float, List['JsonValue'], Dict[str, 'JsonValue']]
JsonType = Union[List[JsonValue], Dict[str, JsonValue]]
JsonMapping = Mapping[str, JsonValue]


class JsonMappingClass(Mapping[str, JsonValue]):

    def __getitem__(self, key: str) -> JsonValue:
        return self.__dict__.__getitem__(key)

    def __len__(self) -> int:
        return self.__dict__.__len__()

    def __iter__(self) -> Iterator[str]:
        return self.__dict__.__iter__()

    def items(self):
        return self.__dict__.items()

    def apply_template(self, template_file: str, encoding='utf-8') -> JsonType:
        return load_template(template_file, encoding=encoding)(self)


def load_template(template_file: str, encoding: str = 'utf-8') -> Callable[[JsonMapping | JsonMappingClass], JsonType]:
    with open(template_file, encoding=encoding) as f:
        t = Template(f.read())

    return lambda mapping: json.loads(
        t.safe_substitute({k: json.dumps(v) for k, v in mapping.items()}))


if __name__ == '__main__':
    json_loader = load_template('template/template.json.tpl')

    params = {
        'int_val': 1,
        'float_val': .2,
        'str_val': '文字列',
        'dict_val': {'key': '値', 'list': [3, 4, 5]},
        'list_val': [1, 2, 3, {'key': 'value'}],
    }

    print(json_loader(params))

    import dataclasses

    @dataclasses.dataclass(frozen=True)
    class ExampleParams(JsonMappingClass):
        int_val: int
        float_val: float
        str_val: str
        dict_val: Dict[str, JsonValue]
        list_val: List[JsonValue]

    params = ExampleParams(
        int_val=1,
        float_val=.3,
        str_val='文字列',
        dict_val={'key': '値', 'list': [3, 4, 5]},
        list_val=[1, 2, 3, {'key': 'value'}]
    )

    print(params.apply_template('template/template.json.tpl'))
