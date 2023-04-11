import inspect
import json
import os
from abc import ABC
from typing import Optional
import yaml
from attr import define, fields, Attribute


@define
class BaseTool(ABC):
    MANIFEST_FILE = "manifest.yml"
    DOCKERFILE_FILE = "Dockerfile"
    REQUIREMENTS_FILE = "requirements.txt"

    @property
    def name(self) -> str:
        return self.__class__.__name__

    @property
    def env_fields(self) -> list[Attribute]:
        return [f for f in fields(self.__class__) if f.metadata.get("env")]

    @property
    def env(self) -> dict[str, str]:
        return {f.metadata["env"]: str(getattr(self, f.name)) for f in self.env_fields}

    @property
    def manifest_path(self) -> str:
        return os.path.join(self.abs_dir_path, self.MANIFEST_FILE)

    @property
    def dockerfile_path(self) -> str:
        return os.path.join(self.abs_dir_path, self.DOCKERFILE_FILE)

    @property
    def requirements_path(self) -> str:
        return os.path.join(self.abs_dir_path, self.REQUIREMENTS_FILE)

    @property
    def manifest(self) -> dict:
        with open(self.manifest_path, "r") as yaml_file:
            return yaml.safe_load(yaml_file)

    @property
    def dockerfile(self) -> Optional[str]:
        if os.path.exists(self.dockerfile_path):
            with open(self.dockerfile_path, "r") as dockerfile:
                return dockerfile.read()
        else:
            return None

    @property
    def abs_file_path(self):
        return os.path.abspath(inspect.getfile(self.__class__))

    @property
    def abs_dir_path(self):
        return os.path.dirname(self.abs_file_path)

    def actions(self) -> list[callable]:
        methods = []

        for name, method in inspect.getmembers(self, predicate=inspect.ismethod):
            if getattr(method, "is_action", False):
                methods.append(method)

        return methods

    def env_value(self, name: str) -> Optional[str]:
        env_var_value = os.environ.get(name, None)
        if env_var_value:
            return env_var_value
        else:
            return next(
                (str(getattr(self, f.name)) for f in self.env_fields if f.metadata.get("env") == name),
                None
            )

    def get_action_name(self, action: callable) -> str:
        if action is None or not getattr(action, "is_action", False):
            raise Exception("This method is not a tool action.")
        else:
            schema = action.config["value_schema"].json_schema("ToolActionSchema")

            return action.config["name"]

    def get_action_description(self, action: callable) -> str:
        if action is None or not getattr(action, "is_action", False):
            raise Exception("This method is not a tool action.")
        else:
            schema = action.config["value_schema"].json_schema("ToolActionSchema")

            return str.join("\n", [
                action.config["description"],
                f"Input schema: {json.dumps(schema)}"
            ])

    def get_action_value_schema(self, action: callable) -> dict:
        if action is None or not getattr(action, "is_action", False):
            raise Exception("This method is not a tool action.")
        else:
            return action.config["value_schema"].json_schema("ToolInputSchema")

    def validate(self) -> bool:
        from griptape.core.utils import ManifestValidator

        if not os.path.exists(self.manifest_path):
            raise Exception(f"{self.MANIFEST_FILE} not found")

        if not os.path.exists(self.requirements_path):
            raise Exception(f"{self.REQUIREMENTS_FILE} not found")

        ManifestValidator().validate(self.manifest)

        return True
