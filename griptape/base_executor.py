import inspect
import os
from abc import ABC, abstractmethod
from griptape import BaseTool


class BaseExecutor(ABC):
    @abstractmethod
    def execute(self, tool_action: callable, value: bytes) -> bytes:
        ...

    def tool_dir(self, tool: BaseTool):
        class_file = inspect.getfile(tool.__class__)

        return os.path.dirname(os.path.abspath(class_file))

    def tool_name(self, tool: BaseTool) -> str:
        return tool.__class__.__name__
