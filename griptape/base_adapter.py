from abc import ABC
from attr import define, field

from griptape import BaseExecutor
from griptape.executors import LocalExecutor


@define
class BaseAdapter(ABC):
    executor: BaseExecutor = field(default=LocalExecutor(), kw_only=True)
