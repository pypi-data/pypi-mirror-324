# ToolMate AI - SDK

ToolMate-SDK: a software developement kit for developing agentic AI applications that support 13 LLM backends and integrate tools and agents. (Developer: Eliran Wong)

Supported backends: anthropic, azure, custom, deepseek, genai, github, googleai, groq, llamacpp, mistral, ollama, openai, vertexai, xai

# A Sibling Project

This SDK incorporates the best aspects of our favorite project, [Toolmate AI](https://github.com/eliranwong/toolmate), to create a library aimed at further advancing the development of AI applications.

# Supported backends

`anthropic` - [Anthropic API](https://console.anthropic.com/)

`azure` - [Azure OpenAI API](https://learn.microsoft.com/en-us/azure/ai-services/openai/reference)

`custom` - any openai-compatible backends

`deepseek` - [DeepSeek API](https://platform.deepseek.com/)

`genai` - [Vertex AI](https://cloud.google.com/vertex-ai) or [Google AI](https://ai.google.dev/)

`github` - [Github API](https://github.com/marketplace/models/azure-openai/gpt-4o)

`googleai` - [Google AI](https://ai.google.dev/)

`groq` - [Groq Cloud API](https://console.groq.com)

`llamacpp` - [Llama.cpp Server](https://github.com/ggerganov/llama.cpp) - [locat setup](https://github.com/ggerganov/llama.cpp/blob/master/docs/build.md) required

`mistral` - [Mistral API](https://console.mistral.ai/api-keys/)

`ollama` - [Ollama](https://ollama.com/) - [local setup](https://ollama.com/download) required

`openai` - [OpenAI API](https://platform.openai.com/)

`vertexai` - [Vertex AI](https://cloud.google.com/vertex-ai)

`xai` - [XAI API](https://x.ai/api)

For simplicity, `toolmate-sdk` uses `ollama` as the default backend, if parameter `backend` is not specified. Ollama models are automatically downloaded if they have not already been downloaded.

# Installation

Basic:

> pip install --upgrade toolmate-sdk

Basic installation supports all AI backends mentioned above, except for `vertexai`.

Extras:

We support Vertex AI via [Google GenAI SDK](https://pypi.org/project/google-genai/).  As this package supports most platforms, except for Android Termux, we separate this package `google-genai` as an extra.  To support Vertex AI with `toolmate-sdk`, install with running:

> pip install --upgrade toolmate-sdk[genai]

# Usage

This SDK is designed to provide a single function for interacting with all AI backends, delivering a unified experience for generating AI responses. The main APIs are provided with the function `generate` located in this [file](https://github.com/eliranwong/toolmate-sdk/blob/main/toolmate_sdk/__init__.py#L28).

Find documentation at https://github.com/eliranwong/toolmate-sdk/tree/main/toolmate_sdk/docs/README.md

# Examples

An example, assuming [Ollama](https://ollama.com/) is [installed](https://ollama.com/download):

'''
from toolmate_sdk import generate

generate("What is AI?")

generate("What is ToolMate AI?", tool="search_google")
'''

Read more examples at:

https://github.com/eliranwong/toolmate-sdk/tree/main/toolmate-sdk/examples

# TODO

* add documentation
* add examples
* convert availble ToolMate AI tools into tools that runable with this SDK
* added built-in system messages
* added built-in predefined contexts
* added built-in prompts
* add cli options for running simple inference, tools or testing
* add agent to handle code generation