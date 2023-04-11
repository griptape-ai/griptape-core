from attr import define, field
from schema import Schema, Literal
from griptape.core import BaseTool, action


@define
class MockTool(BaseTool):
    configs = {
        "test": {
            "name": "test",
            "description": "test description",
            "value_schema": Schema({
                Literal(
                    "value",
                    description="Test input"
                ): str
            }),
            "foo": "bar"
        }
    }

    test_field: str = field(default="test", kw_only=True, metadata={"env": "TEST_FIELD"})

    @action(config=configs["test"])
    def test(self, value: bytes) -> str:
        return f"ack {value.decode()}"
