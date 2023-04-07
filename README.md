# Griptape

[![Tests](https://github.com/griptape-ai/griptape-core/actions/workflows/tests.yml/badge.svg)](https://github.com/griptape-ai/griptape-core/actions/workflows/tests.yml)
[![Docs](https://readthedocs.org/projects/griptape/badge/)](https://griptape.readthedocs.io)
[![PyPI Version](https://img.shields.io/pypi/v/griptape-core.svg)](https://pypi.python.org/pypi/griptape-core)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://github.com/gitbucket/gitbucket/blob/master/LICENSE)

Griptape is a Python framework that enables developers to write tools for generative AI middleware once and use it anywhere.

Griptape has three core components:

- **Tools**: call external APIs, access databases, and run arbitrary code or CLI commands.
- **Executors**: run your tools safely in any environment: local, containerized, or serverless in the cloud.
- **Adapters**: convert tools into underlying middleware abstractions, such as ChatGPT Plugins, LangChain tools, and Fixie.ai agents.

## Getting Started

Griptape separates the core framework from tools into two Python packages: `griptape-core` and `griptape-tools`. Explore Griptape tools in the [griptape-tools repo](https://github.com/griptape-ai/griptape-tools)

First, install those packages:

```
pip install griptape-core
pip install griptape-tools
```

Next, initialize an executor and some tools:

```python
from griptape.core.adapters import LangchainToolAdapter, ChatgptPluginAdapter
from griptape.core.executors import LocalExecutor
from griptape.tools import (
    Calculator, GoogleSearch
)

tool_executor = LocalExecutor()

google_search = GoogleSearch(
    api_search_key="<search key>",
    api_search_id="<search ID>"
)
calculator = Calculator()
```

You can execute tool actions directly:

```python
tool_executor.execute(calculator.calculate, "42**42".encode())
```

Convert tool actions into LangChain tools:

```python
agent = initialize_agent(
    [
        LangchainToolAdapter(executor=tool_executor).generate(google_search.search),
        LangchainToolAdapter(executor=tool_executor).generate(calculator.calculate)
    ],
    OpenAI(temperature=0.5, model_name="text-davinci-003"),
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

agent.run("What is 42^42?")
```

Or generate and run a ChatGPT Plugin:

```python
app = ChatgptPluginAdapter(
    host="localhost:8000",
    path_prefix="/search-tool/",
    executor=tool_executor
).generate_api(google_search)

# run with `uvicorn app:app --reload`
```

## Contributing

Contributions in the form of bug reports, feature ideas, or pull requests are super welcome! Take a look at the current issues and if you'd like to help please submit a pull request with some tests.

## License

Griptape is available under the Apache 2.0 License.