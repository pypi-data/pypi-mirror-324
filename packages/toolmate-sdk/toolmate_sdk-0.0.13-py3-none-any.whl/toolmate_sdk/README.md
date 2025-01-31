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

`github` - [Github API](https://docs.github.com/en/github-models/prototyping-with-ai-models#experimenting-with-ai-models-using-the-api)

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

This SDK is designed to provide a single function for interacting with all AI backends, delivering a unified experience for generating AI responses. The main APIs are provided with the function `generate` located in this [file](https://github.com/eliranwong/toolmate-sdk/blob/main/toolmate_sdk/__init__.py#L29).

Find documentation at https://github.com/eliranwong/toolmate-sdk/blob/main/docs/README.md

# Examples

The following examples assumes [Ollama](https://ollama.com/) is [installed](https://ollama.com/download):

To import:

> from toolmate_sdk import generate

To generate, e.g.:

> generate("What is AI?")

> generate("What is ToolMate AI?", tool="search_google")

> generate("How many 'r's are there in the word 'strawberry'?", tool="task")

> generate("What time is it right now?", tool="task")

> generate("Open github.com in a web browser.", tool="task")

> generate("Convert file 'music.wav' into mp3 format.", tool="task")

> generate("Send an email to Eliran Wong at eliran.wong@domain.com to express my gratitude for his work.", tool="send_gmail")

> generate("Is it better to drink wine in the morning, afternoon, or evening?", context="reflect", stream=True)

> generate("Is it better to drink wine in the morning, afternoon, or evening?", context="think", follow_up_prompt=["review", "refine"], stream=True)

> generate("Provide a detailed introduction to generative AI.", system=["create_agents", "assign_agents"], follow_up_prompt="Who is the best agent to contribute next?", stream=True, model="llama3.3:70b")

These are just a few simple and straightforward examples.  You may find more examples at:

https://github.com/eliranwong/toolmate-sdk/tree/main/toolmate-sdk/examples

# TODO

* add documentation about tool creation
* add examples
* convert availble ToolMate AI tools into tools that runable with this SDK
* added built-in system messages
* added built-in predefined contexts
* added built-in prompts
* add cli options for running simple inference, tools or testing
* improve code generation handling
