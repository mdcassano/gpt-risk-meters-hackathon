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
            if "error" not in spec:
                yield GenerateQueryTest.from_parent(
                    self,
                    name=spec["name"],
                    description=spec["description"],
                    query=spec["query"],
                )
                yield DescribeQueryTest.from_parent(
                    self,
                    name=spec["name"],
                    description=spec["description"],
                    query=spec["query"],
                )
            else:
                yield ErrorQueryTest.from_parent(
                    self,
                    name=spec["name"],
                    description=spec["description"],
                    error=spec["error"],
                )


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


class ErrorQueryTest(pytest.Item):
    def __init__(self, name, parent, description, error):
        super().__init__(name, parent)
        self.name = name
        self.description = description
        self.error = error

    def runtest(self):
        try:
            Chat(self.description, prefix="").syntax_output()
        except Exception as ex:
            assert self.error in str(ex)

    def reportinfo(self):
        return self.path, 0, self.name


class DescribeQueryTest(pytest.Item):
    def __init__(self, name, parent, description, query):
        super().__init__(name, parent)
        self.name = name
        self.description = description
        self.query = query

    def runtest(self):
        self.generated_description = Chat(
            self.description, prefix="reverse"
        ).description_output()
        self.round_trip_query = Chat(
            self.generated_description, prefix=""
        ).syntax_output()
        if self.generated_description and self.round_trip_query:
            assert self.query == self.round_trip_query
        else:
            pytest.skip("No description generated")

    def repr_failure(self, excinfo):
        """Called when self.runtest() raises an exception."""
        if isinstance(excinfo.value, AssertionError):
            return "\n".join(
                [
                    "Failed to round-trip the generated description:",
                    "   -> query input: {0!r}".format(self.query),
                    "     -> description: {0!r}".format(self.generated_description),
                    "       -> query output: {0!r}".format(self.round_trip_query),
                    "   spec failed: {0!r}".format(excinfo.value),
                ]
            )

    def reportinfo(self):
        return self.path, 0, self.name
