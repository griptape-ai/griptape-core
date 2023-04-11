from attr import define, field
from schema import Schema, Literal
from griptape.core import BaseTool, action


@define
class InvalidMockTool(BaseTool):
    configs = {
        "test": {
            # no name should make this tool invalid
            #"name": "test",
            "description": "test description",
            "input_schema": Schema({
                Literal(
                    "input",
                    description="Test input"
                ): str
            }),
            "foo": "bar"
        }
    }

    test_field: str = field(default="test", kw_only=True, metadata={"env": "TEST_FIELD"})

    @action(config=configs["test"])
    def test(self, action_input: bytes) -> str:
        return f"ack {action_input.decode()}"
