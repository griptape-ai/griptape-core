import logging
from attrs import define, field
import docker
from docker.errors import NotFound
import griptape
from griptape import BaseExecutor, BaseTool
import stringcase


@define
class DockerExecutor(BaseExecutor):
    DEFAULT_DOCKERFILE_DIR = "resources/docker_executor"
    client: docker.DockerClient = field(default=docker.from_env(), kw_only=True)

    def execute(self, tool_action: callable, value: bytes) -> bytes:
        tool = tool_action.__self__

        self.build_image(tool)
        self.remove_existing_container(self.container_name(tool))

        return self.run_container(tool_action, value).encode()

    def run_container(self, tool_action: callable, value: bytes) -> str:
        tool = tool_action.__self__
        workdir = "/tool"
        tool_name = self.tool_name(tool)
        command = [
            "python",
            "-c",
            f'from tool import {tool_name}; print({tool_name}().{tool_action.__name__}({value}))'
        ]
        binds = {
            self.tool_dir(tool): {
                "bind": workdir,
                "mode": "rw"
            }
        }

        result = self.client.containers.run(
            self.image_name(tool),
            environment=tool.env,
            command=command,
            name=self.container_name(tool),
            volumes=binds,
            remove=True
        )

        return result.decode().strip()

    def remove_existing_container(self, name: str) -> None:
        try:
            existing_container = self.client.containers.get(name)
            existing_container.remove(force=True)

            logging.info(f"Removed existing container: {name}")
        except NotFound:
            pass

    def build_image(self, tool: BaseTool) -> None:
        image = self.client.images.build(
            path=self.tool_dir(tool) if tool.dockerfile else griptape.abs_path(self.DEFAULT_DOCKERFILE_DIR),
            tag=self.image_name(tool),
            rm=True,
            forcerm=True
        )

        response = [line for line in image]

        logging.info(f"Built image: {response[0].short_id}")

    def image_name(self, tool: BaseTool) -> str:
        return f"{stringcase.snakecase(self.tool_name(tool))}_image"

    def container_name(self, tool: BaseTool) -> str:
        return f"{stringcase.snakecase(self.tool_name(tool))}_container"
