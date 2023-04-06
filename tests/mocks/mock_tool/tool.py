from attr import define, field
from schema import Schema, Literal
from griptape import BaseTool, action


@define
class MockTool(BaseTool):
    schemas = {
        "test": Schema({
            Literal(
                "action_input",
                description="Test input"
            ): str
        })
    }

    test_field: str = field(default="test", kw_only=True, metadata={"env": "TEST_FIELD"})

    @action(name="test", schema=schemas["test"])
    def test(self, action_input: bytes) -> str:
        return f"ack {action_input.decode()}"
