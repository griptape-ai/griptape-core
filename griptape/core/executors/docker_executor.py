import logging
from typing import Optional
from attr import define, field, Factory
import docker
from docker.errors import NotFound
import griptape
from griptape.core import BaseTool
from griptape.core import BaseExecutor
import stringcase
import tempfile
import shutil
import os


@define
class DockerExecutor(BaseExecutor):
    DEFAULT_DOCKERFILE_DIR = "resources/docker_executor"
    client: docker.DockerClient = field(
        default=Factory(lambda self: self.default_docker_client(), takes_self=True),
        kw_only=True
    )

    def default_docker_client(self) -> Optional[docker.DockerClient]:
        try:
            return docker.from_env()
        except Exception as e:
            logging.error(e)

            return None

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
        with tempfile.TemporaryDirectory() as temp_dir:
            shutil.rmtree(temp_dir)
            shutil.copytree(self.tool_dir(tool), temp_dir)

            if not tool.dockerfile:
                dockerfile_path = griptape.abs_path(os.path.join(self.DEFAULT_DOCKERFILE_DIR, tool.DOCKERFILE_FILE))

                shutil.copy(dockerfile_path, temp_dir)

            image = self.client.images.build(
                path=temp_dir,
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
