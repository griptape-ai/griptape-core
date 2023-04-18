# griptape-core

[![Tests](https://github.com/griptape-ai/griptape-core/actions/workflows/tests.yml/badge.svg)](https://github.com/griptape-ai/griptape-core/actions/workflows/tests.yml)
[![PyPI Version](https://img.shields.io/pypi/v/griptape-core.svg)](https://pypi.python.org/pypi/griptape-core)
[![Docs](https://readthedocs.org/projects/griptape/badge/)](https://griptape.readthedocs.io/en/latest/griptape-core/)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://github.com/gitbucket/gitbucket/blob/master/LICENSE)

**griptape-core** is a Python framework that enables developers to write tools for generative AI middleware once and use it anywhere.

**griptape-core** is part of [griptape](https://github.com/griptape-ai/griptape), a modular Python framework for integrating data, APIs, tools, memory, and chain of thought reasoning into LLMs.

**griptape-core** has three core components:

- **Tools**: call external APIs, access databases, and run arbitrary code or CLI commands.
- **Executors**: run your tools safely in any environment: local, containerized, or serverless in the cloud.
- **Adapters**: convert tools into underlying middleware abstractions, such as ChatGPT Plugins, LangChain tools, and Fixie.ai agents.

## Documentation

Please refer to [Griptape Docs](https://griptape.readthedocs.io) for:

- Getting started guides. 
- Core concepts and design overviews.
- Examples.
- Contribution guidelines.

## License

griptape-core is available under the Apache 2.0 License.
