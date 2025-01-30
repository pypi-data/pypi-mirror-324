import yaml

from source_faker.models import ColumnType


class Dumper(yaml.Dumper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.add_representer(ColumnType, self.represent_column_type)

    def increase_indent(self, flow=False, indentless=False):
        return super(Dumper, self).increase_indent(flow, False)

    @staticmethod
    def represent_column_type(dumper, obj):
        return dumper.represent_scalar(
            'tag:yaml.org,2002:str',
            obj.value
        )

    def ignore_aliases(self, data):
        return True
