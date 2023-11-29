import pytest

from functools import partial
from chat import Chat

def pytest_collect_file(parent, file_path):
    if file_path.suffix == ".yaml" and file_path.name.startswith("test"):
        return YamlFile.from_parent(parent, path=file_path)

class YamlFile(pytest.File):
    def collect(self):
        import yaml  # only import pyyaml if necessary
        raw = yaml.safe_load(self.path.open())
        for spec in raw:
            yield GenerateQueryTest.from_parent(self, name=spec['name'], description=spec['description'], query=spec['query'])
            yield DescribeQueryTest.from_parent(self, name=spec['name'], description=spec['description'], query=spec['query'])

class GenerateQueryTest(pytest.Item):
    def __init__(self, name, parent, description, query):
        super().__init__(name, parent)
        self.name = name
        self.description = description
        self.query = query

    def runtest(self):
        assert self.query == Chat(self.description, prefix="").syntax_output()

    def reportinfo(self):
        return self.path, 0, self.name

class DescribeQueryTest(pytest.Item):
    def __init__(self, name, parent, description, query):
        super().__init__(name, parent)
        self.name = name
        self.description = description
        self.query = query

    def generated_description(self):
        return Chat(self.description, prefix="reverse").description_output()

    def runtest(self):
        assert self.query == Chat(self.generated_description(), prefix="").syntax_output()

    def repr_failure(self, excinfo):
        """Called when self.runtest() raises an exception."""
        breakpoint()
        return "\n".join(
            [
                "Failed to round-trip the generated description:",
                "   spec failed: {1!r}: {2!r}".format(*excinfo.value.args),
                "   no further details known at this point.",
            ]
        )

    def reportinfo(self):
        return self.path, 0, self.name