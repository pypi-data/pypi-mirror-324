from .backends.anthropic import AnthropicLLM
from .backends.azure import AzureLLM
from .backends.custom import OpenaiCompatibleLLM
from .backends.deepseek import DeepseekLLM
from .backends.genai import GenaiLLM
from .backends.github import GithubLLM
from .backends.googleai import GoogleaiLLM
from .backends.groq import GroqLLM
from .backends.llamacpp import LlamacppLLM
from .backends.mistral import MistralLLM
from .backends.ollama import OllamaLLM
from .backends.openai import OpenaiLLM
from .backends.xai import XaiLLM

from .utils.instructions import getRagPrompt
from .utils.retrieve_text_output import getChatCompletionText
from .utils.handle_text import readTextFile

from typing import Optional, Callable, Union, Any, List, Dict
from copy import deepcopy
from io import StringIO
import sys, os, json, traceback

PACKAGE_PATH = os.path.dirname(os.path.realpath(__file__))
PACKAGE_NAME = os.path.basename(PACKAGE_PATH)
SUPPORTED_BACKENDS = ["anthropic", "azure", "custom", "deepseek", "genai", "github", "googleai", "groq", "llamacpp", "mistral", "ollama", "openai", "vertexai", "xai"]
DEVELOPER_MODE = True if os.getenv("DEVELOPER_MODE") == "TRUE" else False

def generate(
        messages: Union[List[Dict[str, str]], str], # user request or messages containing user request; accepts either a single string or a list of dictionaries
        backend: Optional[str]="ollama", # AI backend; check SUPPORTED_BACKENDS for supported backends
        model: Optional[str]=None, # AI model name; applicable to all backends, execept for llamacpp
        model_keep_alive: Optional[str]=None, # time to keep the model loaded in memory; applicable to ollama only
        system: Optional[Union[List[str], str]]=None, # system message; define how the model should generally behave and respond; accepts a list of strings or a single string; loop through multiple system messages for multi-turn inferences if it is a list
        context: Optional[Union[List[str], str]]=None, # predefined context to be added to the user prompt as prefix; accepts a list of strings or a single string; loop through multiple predefined contexts for multi-turn inferences if it is a list
        follow_up_prompt: Optional[Union[List[str], str]]=None, # follow-up prompts after an assistant message is generated; accepts a list of strings or a single string; loop through multiple follow-up prompts for multi-turn inferences if it is a list
        tool: Optional[Union[List[str], str]]=None, # a tool either a built-in tool name under the folder `tools` in the package directory or a file path of the tool; accepts a list of strings or a single string; loop through multiple tools for multi-turn actions if it is a list; parameters of both `schema` and `func` are ignored when `tool` parameter is given
        schema: Optional[dict]=None, # json schema for structured output or function calling
        func: Optional[Callable[..., Optional[str]]]=None, # function to be called
        temperature: Optional[float]=None, # temperature for sampling
        max_tokens: Optional[int]=None, # maximum number of tokens to generate
        context_window: Optional[int]=None, # context window size; applicable to ollama only
        batch_size: Optional[int]=None, # batch size; applicable to ollama only
        prefill: Optional[Union[List[str], str]]=None, # prefill of assistant message; applicable to deepseek, mistral, ollama and groq only; accepts a list of strings or a single string; loop through multiple prefills for multi-turn inferences if it is a list
        stop: Optional[list]=None, # stop sequences
        stream: Optional[bool]=False, # stream partial message deltas as they are available
        stream_events_only: Optional[bool]=False, # return streaming events object only
        api_key: Optional[str]=None, # API key or credentials json file path in case of using Vertex AI as backend; applicable to anthropic, custom, deepseek, genai, github, googleai, groq, mistral, openai, xai
        api_endpoint: Optional[str]=None, # API endpoint; applicable to anthropic, azure, custom, llamacpp, ollama
        api_project_id: Optional[str]=None, # project id; applicable to Vertex AI only, i.e., vertexai or genai
        api_service_location: Optional[str]=None, # cloud service location; applicable to Vertex AI only, i.e., vertexai or genai
        api_timeout: Optional[Union[int, float]]=None, # timeout for API request; applicable to backends, execept for ollama, genai and vertexai
        print_on_terminal: Optional[bool]=True, # print output on terminal
        word_wrap: Optional[bool]=True, # word wrap output according to current terminal width
        **kwargs, # pass extra options supported by individual backends
) -> Union[List[Dict[str, str]], Any]:
    """
    Generate AI assistant response.

    Args:
        messages:
            type: Union[List[Dict[str, str]], str]
            user request or messages containing user request
            accepts either a single string or a list of dictionaries
            use a single string string to specify user request without chat history
            use a list of dictionaries to provide with the onging interaction between user and assistant
            when a list is given:
                each dictionary in the list should contain keys `role` and `content`
                specify the latest user request in the last item content
                list format example:
                    [
                        {"role": "system", "You are an AI assistant."},
                        {"role": "user", "Hello!"},
                        {"role": "assistant", "Hello! How can I assist you today?"},
                        {"role": "user", "What is generative AI?"}
                    ]

        backend:
            type: Optional[str]="ollama"
            AI backend
            supported backends: "anthropic", "azure", "custom", "deepseek", "genai", "github", "googleai", "groq", "llamacpp", "mistral", "ollama", "openai", "vertexai", "xai"

        model:
            type: Optional[str]=None
            AI model name
            applicable to all backends, execept for `llamacpp`
            for backend `llamacpp`, specify a model file in the command line running the llama.cpp server
            for backend `ollama`, model is automatically downloaded if it is not in the downloaded model list

        model_keep_alive:
            type: Optional[str]=None
            time to keep the model loaded in memory
            applicable to ollama only

        system:
            type: Optional[Union[List[str], str]]=None
            system message
            define how the model should generally behave and respond
            accepts a list of strings or a single string
            loop through multiple system messages for multi-turn inferences if it is a list

        context:
            type: Optional[Union[List[str], str]]=None
            predefined context to be added to the user prompt as prefix
            accepts a list of strings or a single string
            loop through multiple predefined contexts for multi-turn inferences if it is a list

        follow_up_prompt:
            type: Optional[Union[List[str], str]]=None
            follow-up prompts after an assistant message is generated
            accepts a list of strings or a single string
            loop through multiple follow-up prompts for multi-turn inferences if it is a list

        tool:
            type: Optional[Union[List[str], str]]=None
            a tool either a built-in tool name under the folder `tools` in the package directory or a file path of the tool
            accepts a list of strings or a single string
            loop through multiple tools for multi-turn actions if it is a list
            parameters of both `schema` and `func` are ignored when `tool` parameter is given

        schema:
            type: Optional[dict]=None
            json schema for structured output or function calling

        func:
            type: Optional[Callable[..., Optional[str]]]=None
            function to be called

        temperature:
            type: Optional[float]=None
            temperature for sampling

        max_tokens:
            type: Optional[int]=None
            maximum number of tokens to generate

        context_window:
            type: Optional[int]=None
            context window size
            applicable to ollama only

        batch_size:
            type: Optional[int]=None
            batch size
            applicable to ollama only

        prefill:
            type: Optional[Union[List[str], str]]=None
            prefill of assistant message
            applicable to deepseek, mistral, ollama and groq only
            accepts a list of strings or a single string
            loop through multiple prefills for multi-turn inferences if it is a list

        stop:
            type: Optional[list]=None
            stop sequences

        stream:
            type: Optional[bool]=False
            stream partial message deltas as they are available

        stream_events_only:
            type: Optional[bool]=False
            return streaming events object only

        api_key:
            type: Optional[str]=None
            API key or credentials json file path in case of using Vertex AI as backend
            applicable to anthropic, custom, deepseek, genai, github, googleai, groq, mistral, openai, xai

        api_endpoint:
            type: Optional[str]=None
            API endpoint
            applicable to anthropic, azure, custom, llamacpp, ollama

        api_project_id:
            type: Optional[str]=None
            project id
            applicable to Vertex AI only, i.e., vertexai or genai

        api_service_location:
            type: Optional[str]=None
            cloud service location
            applicable to Vertex AI only, i.e., vertexai or genai

        api_timeout:
            type: Optional[Union[int, float]]=None
            timeout for API request
            applicable to backends, execept for ollama, genai and vertexai

        print_on_terminal:
            type: Optional[bool]=True
            print output on terminal

        word_wrap:
            type: Optional[bool]=True
            word wrap output according to current terminal width

        **kwargs,
            pass extra options supported by individual backends

    Return:
        either:
            list of messages containing multi-turn interaction between user and the AI assistant
            find the latest assistant response in the last item of the list
        or:
            streaming events object of AI assistant response when both parameters `stream` and `stream_events_only` are set to `True`
    """
    if backend not in SUPPORTED_BACKENDS:
        raise ValueError(f"Backend {backend} is not supported. Supported backends are {SUPPORTED_BACKENDS}")
    # placeholders
    original_system = ""
    chat_system = ""
    # deep copy messages avoid modifying the original one
    messagesCopy = deepcopy(messages) if isinstance(messages, list) else [{"role": "system", "content": "You are a helpful AI assistant."}, {"role": "user", "content": messages}]
    # handle given system message(s)
    if system:
        if isinstance(system, list):
            system_instruction = system.pop(0)
        else: # a string instead
            system_instruction = system
            system = []
        # check if it is a predefined system message built-in with this SDK
        possible_system_file_path = os.path.join(PACKAGE_PATH, "systems", f"{system_instruction}.md")
        if os.path.isfile(possible_system_file_path):
            system_file_content = readTextFile(possible_system_file_path)
            if system_file_content:
                system_instruction = system_file_content
        elif os.path.isfile(system_instruction): # system_instruction itself is a valid filepath
            system_file_content = readTextFile(system_instruction)
            if system_file_content:
                system_instruction = system_file_content
        original_system = updateSystemMessage(messagesCopy, system_instruction)
    # handle given predefined context(s)
    if context:
        if isinstance(context, list):
            context_content = context.pop(0)
        else: # a string instead
            context_content = context
            context = []
        # check if it is a predefined context built-in with this SDK
        possible_context_file_path = os.path.join(PACKAGE_PATH, "contexts", f"{context_content}.md")
        if os.path.isfile(possible_context_file_path):
            context_file_content = readTextFile(possible_context_file_path)
            if context_file_content:
                context_content = context_file_content
        elif os.path.isfile(context_content): # context_content itself is a valid filepath
            context_file_content = readTextFile(context_content)
            if context_file_content:
                context_content = context_file_content
        messagesCopy[-1] = context_content + messagesCopy[-1]
    # handle given prefill(s)
    if prefill:
        if isinstance(prefill, list):
            prefill_content = prefill.pop(0)
        else: # a string instead
            prefill_content = prefill
            prefill = None
    else:
        prefill_content = None
    # handle given tools
    if tool:
        if isinstance(tool, list):
            tool_entity = tool.pop(0)
        else: # a string instead
            tool_entity = tool
            tool = []
        tool_name = tool_entity[:20]
        # check if it is a predefined tool built-in with this SDK
        possible_tool_file_path = os.path.join(PACKAGE_PATH, "tools", f"{tool_entity}.py")
        if os.path.isfile(possible_tool_file_path):
            tool_file_content = readTextFile(possible_tool_file_path)
            if tool_file_content:
                tool_entity = tool_file_content
        elif os.path.isfile(tool_entity): # tool_entity itself is a valid filepath
            tool_file_content = readTextFile(tool_entity)
            if tool_file_content:
                tool_entity = tool_file_content
        try:
            exec(tool_entity, globals())
            tool_system = TOOL_SYSTEM
            schema = TOOL_SCHEMA
            func = TOOL_METHOD
            if tool_system:
                chat_system = updateSystemMessage(messagesCopy, tool_system)
        except Exception as e:
            print(f"Failed to execute tool `{tool_name}`! An error occurred: {e}")
            if DEVELOPER_MODE:
                print(traceback.format_exc())
    # deep copy schema avoid modifying the original one
    schemaCopy = None if schema is None else deepcopy(schema)
    # run LLM
    if schemaCopy is not None: # structured output or function calling; allow schema to be an empty dict
        dictionary_output = {} if not schemaCopy else getDictionaryOutput(
            messagesCopy,
            schemaCopy,
            backend,
            model=model,
            model_keep_alive=model_keep_alive,
            temperature=temperature,
            max_tokens=max_tokens,
            context_window=context_window,
            batch_size=batch_size,
            prefill=prefill_content,
            stop=stop,
            api_key=api_key,
            api_endpoint=api_endpoint,
            api_project_id=api_project_id,
            api_service_location=api_service_location,
            api_timeout=api_timeout,
            **kwargs
        )
        if chat_system:
            updateSystemMessage(messagesCopy, chat_system)
            chat_system = ""
        if func:
            # Create a StringIO object to capture the output
            terminal_output = StringIO()
            # Redirect stdout to the StringIO object
            old_stdout = sys.stdout
            sys.stdout = terminal_output
            # placeholder for function text output
            function_text_output = ""
            try:
                # execute the function
                function_response = func() if not dictionary_output else func(**dictionary_output) # returned response can be either 1) an empty string: no chat extension 2) a non-empty string: chat extension 3) none: errors encountered in executing the function
                function_text_output = terminal_output.getvalue() # capture the function text output for function calling without chat extension
            except:
                function_response = None # due to unexpected errors encountered in executing the function; fall back to regular completion
            # Restore the original stdout
            sys.stdout = old_stdout
            # handle function response
            if function_response is None or function_response: # fall back to regular completion if function_response is None; chat extension if function_response
                return generate(
                    addContextToMessages(messagesCopy, function_response) if function_response else messagesCopy,
                    backend,
                    model=model,
                    model_keep_alive=model_keep_alive,
                    system=None if function_response else system,
                    context=None if function_response else context,
                    follow_up_prompt=None if function_response else follow_up_prompt,
                    tool=None if function_response else tool,
                    temperature=temperature,
                    max_tokens=max_tokens,
                    context_window=context_window,
                    batch_size=batch_size,
                    prefill=None if function_response else prefill_content,
                    stop=stop,
                    stream=stream,
                    stream_events_only=stream_events_only,
                    api_key=api_key,
                    api_endpoint=api_endpoint,
                    api_project_id=api_project_id,
                    api_service_location=api_service_location,
                    api_timeout=api_timeout,
                    print_on_terminal=print_on_terminal,
                    word_wrap=word_wrap,
                    **kwargs
                )
            else: # empty str; function executed successfully without chat extension
                output = function_text_output if function_text_output else "Done!"
        else: # structured output
            output = json.dumps(dictionary_output)
        if print_on_terminal:
            print(output)
    else: # regular completion
        if backend == "anthropic":
            completion = AnthropicLLM.getChatCompletion(
                messagesCopy,
                model=model,
                schema=schemaCopy,
                temperature=temperature,
                max_tokens=max_tokens,
                stop=stop,
                stream=stream,
                api_key=api_key,
                api_timeout=api_timeout,
                **kwargs
            )
        elif backend == "azure":
            completion = AzureLLM.getChatCompletion(
                messagesCopy,
                model=model,
                schema=schemaCopy,
                temperature=temperature,
                max_tokens=max_tokens,
                stop=stop,
                stream=stream,
                api_key=api_key,
                api_endpoint=api_endpoint,
                api_timeout=api_timeout,
                **kwargs
            )
        elif backend == "custom":
            completion = OpenaiCompatibleLLM.getChatCompletion(
                messagesCopy,
                model=model,
                schema=schemaCopy,
                temperature=temperature,
                max_tokens=max_tokens,
                stop=stop,
                stream=stream,
                api_key=api_key,
                api_endpoint=api_endpoint,
                api_timeout=api_timeout,
                **kwargs
            )
        elif backend == "deepseek":
            completion = DeepseekLLM.getChatCompletion(
                messagesCopy,
                model=model,
                schema=schemaCopy,
                temperature=temperature,
                max_tokens=max_tokens,
                prefill=prefill_content,
                stop=stop,
                stream=stream,
                api_key=api_key,
                api_timeout=api_timeout,
                **kwargs
            )
        elif backend in ("genai", "vertexai"):
            completion = GenaiLLM.getChatCompletion(
                messagesCopy,
                model=model,
                schema=schemaCopy,
                temperature=temperature,
                max_tokens=max_tokens,
                stop=stop,
                stream=stream,
                api_key=api_key,
                api_project_id=api_project_id,
                api_service_location=api_service_location,
                **kwargs
            )
        elif backend == "github":
            completion = GithubLLM.getChatCompletion(
                messagesCopy,
                model=model,
                schema=schemaCopy,
                temperature=temperature,
                max_tokens=max_tokens,
                stop=stop,
                stream=stream,
                api_key=api_key,
                api_timeout=api_timeout,
                **kwargs
            )
        elif backend == "googleai":
            completion = GoogleaiLLM.getChatCompletion(
                messagesCopy,
                model=model,
                schema=schemaCopy,
                temperature=temperature,
                max_tokens=max_tokens,
                stop=stop,
                stream=stream,
                api_key=api_key,
                api_timeout=api_timeout,
                **kwargs
            )
        elif backend == "groq":
            completion = GroqLLM.getChatCompletion(
                messagesCopy,
                model=model,
                schema=schemaCopy,
                temperature=temperature,
                max_tokens=max_tokens,
                prefill=prefill_content,
                stop=stop,
                stream=stream,
                api_key=api_key,
                api_timeout=api_timeout,
                **kwargs
            )
        elif backend == "llamacpp":
            completion = LlamacppLLM.getChatCompletion(
                messagesCopy,
                schema=schemaCopy,
                temperature=temperature,
                max_tokens=max_tokens,
                stop=stop,
                stream=stream,
                api_endpoint=api_endpoint,
                api_timeout=api_timeout,
                **kwargs
            )
        elif backend == "mistral":
            completion = MistralLLM.getChatCompletion(
                messagesCopy,
                model=model,
                schema=schemaCopy,
                temperature=temperature,
                max_tokens=max_tokens,
                prefill=prefill_content,
                stop=stop,
                stream=stream,
                api_key=api_key,
                api_timeout=api_timeout,
                **kwargs
            )
        elif backend == "ollama":
            completion = OllamaLLM.getChatCompletion(             
                messagesCopy,
                model=model,
                model_keep_alive=model_keep_alive,
                schema=schemaCopy,
                temperature=temperature,
                max_tokens=max_tokens,
                context_window=context_window,
                batch_size=batch_size,
                prefill=prefill_content,
                stop=stop,
                stream=stream,
                api_endpoint=api_endpoint,
                **kwargs
            )
        elif backend == "openai":
            completion = OpenaiLLM.getChatCompletion(
                messagesCopy,
                model=model,
                schema=schemaCopy,
                temperature=temperature,
                max_tokens=max_tokens,
                stop=stop,
                stream=stream,
                api_key=api_key,
                api_timeout=api_timeout,
                **kwargs
            )
        elif backend == "xai":
            completion = XaiLLM.getChatCompletion(
                messagesCopy,
                model=model,
                schema=schemaCopy,
                temperature=temperature,
                max_tokens=max_tokens,
                stop=stop,
                stream=stream,
                api_key=api_key,
                api_timeout=api_timeout,
                **kwargs
            )
        done = True if not follow_up_prompt and not system and not context and not tool and not prefill else False
        if stream and stream_events_only and done:
            return completion
        output = getChatCompletionText(backend, completion, stream=stream, print_on_terminal=print_on_terminal, word_wrap=word_wrap)
        # update the message list
        messagesCopy.append({"role": "assistant", "content": output})
        if original_system:
            updateSystemMessage(messagesCopy, original_system)
        # work on follow-up prompts
        if not done and not follow_up_prompt:
            follow_up_prompt = "Tell me more"
        if follow_up_prompt:
            if isinstance(follow_up_prompt, list):
                follow_up_prompt_content = follow_up_prompt.pop(0)
            else: # a string instead
                follow_up_prompt_content = follow_up_prompt
                follow_up_prompt = []
            # check if it is a predefined follow_up_prompt built-in with this SDK
            possible_follow_up_prompt_file_path = os.path.join(PACKAGE_PATH, "prompts", f"{follow_up_prompt_content}.md")
            if os.path.isfile(possible_follow_up_prompt_file_path):
                follow_up_prompt_file_content = readTextFile(possible_follow_up_prompt_file_path)
                if follow_up_prompt_file_content:
                    follow_up_prompt_content = follow_up_prompt_file_content
            elif os.path.isfile(follow_up_prompt_content): # follow_up_prompt_content itself is a valid filepath
                follow_up_prompt_file_content = readTextFile(follow_up_prompt_content)
                if follow_up_prompt_file_content:
                    follow_up_prompt_content = follow_up_prompt_file_content
            messagesCopy.append({"role": "user", "content": follow_up_prompt_content})
            return generate(
                messages=messagesCopy,
                backend=backend,
                model=model,
                model_keep_alive=model_keep_alive,
                system=system,
                context=context,
                follow_up_prompt=follow_up_prompt,
                tool=tool,
                temperature=temperature,
                max_tokens=max_tokens,
                context_window=context_window,
                batch_size=batch_size,
                prefill=prefill,
                stop=stop,
                stream=stream,
                stream_events_only=stream_events_only,
                api_key=api_key,
                api_endpoint=api_endpoint,
                api_project_id=api_project_id,
                api_service_location=api_service_location,
                api_timeout=api_timeout,
                print_on_terminal=print_on_terminal,
                word_wrap=word_wrap,
                **kwargs
            )
    return messagesCopy

def getDictionaryOutput(
        messages: List[Dict[str, str]],
        schema: dict,
        backend: str,
        model: Optional[str]=None,
        model_keep_alive: Optional[str]=None,
        temperature: Optional[float]=None, 
        max_tokens: Optional[int]=None,
        context_window: Optional[int]=None,
        batch_size: Optional[int]=None,
        prefill: Optional[str]=None,
        stop: Optional[list]=None,
        api_key: Optional[str]=None,
        api_endpoint: Optional[str]=None,
        api_project_id: Optional[str]=None,
        api_service_location: Optional[str]=None,
        api_timeout: Optional[Union[int, float]]=None,
        **kwargs,
) -> dict:
    if backend == "anthropic":
        return AnthropicLLM.getDictionaryOutput(
            messages,
            schema,
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
            stop=stop,
            api_key=api_key,
            api_timeout=api_timeout,
            **kwargs
        )
    elif backend == "azure":
        return AzureLLM.getDictionaryOutput(
            messages,
            schema,
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
            stop=stop,
            api_key=api_key,
            api_endpoint=api_endpoint,
            api_timeout=api_timeout,
            **kwargs
        )
    elif backend == "custom":
        return OpenaiCompatibleLLM.getDictionaryOutput(
            messages,
            schema,
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
            stop=stop,
            api_key=api_key,
            api_endpoint=api_endpoint,
            api_timeout=api_timeout,
            **kwargs
        )
    elif backend == "deepseek":
        return DeepseekLLM.getDictionaryOutput(
            messages,
            schema,
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
            prefill=prefill,
            stop=stop,
            api_key=api_key,
            api_timeout=api_timeout,
            **kwargs
        )
    elif backend in ("genai", "vertexai"):
        return GenaiLLM.getDictionaryOutput(
            messages,
            schema,
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
            stop=stop,
            api_key=api_key,
            api_project_id=api_project_id,
            api_service_location=api_service_location,
            **kwargs
        )
    elif backend == "github":
        return GithubLLM.getDictionaryOutput(
            messages,
            schema,
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
            stop=stop,
            api_key=api_key,
            api_timeout=api_timeout,
            **kwargs
        )
    elif backend == "googleai":
        return GoogleaiLLM.getDictionaryOutput(
            messages,
            schema,
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
            stop=stop,
            api_key=api_key,
            api_timeout=api_timeout,
            **kwargs
        )
    elif backend == "groq":
        return GroqLLM.getDictionaryOutput(
            messages,
            schema,
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
            prefill=prefill,
            stop=stop,
            api_key=api_key,
            api_timeout=api_timeout,
            **kwargs
        )
    elif backend == "llamacpp":
        return LlamacppLLM.getDictionaryOutput(
            messages,
            schema,
            temperature=temperature,
            max_tokens=max_tokens,
            stop=stop,
            api_endpoint=api_endpoint,
            api_timeout=api_timeout,
            **kwargs
        )
    elif backend == "mistral":
        return MistralLLM.getDictionaryOutput(
            messages,
            schema,
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
            prefill=prefill,
            stop=stop,
            api_key=api_key,
            api_timeout=api_timeout,
            **kwargs
        )
    elif backend == "ollama":
        return OllamaLLM.getDictionaryOutput(
            messages,
            schema,
            model=model,
            model_keep_alive=model_keep_alive,
            temperature=temperature,
            max_tokens=max_tokens,
            context_window=context_window,
            batch_size=batch_size,
            prefill=prefill,
            stop=stop,
            api_endpoint=api_endpoint,
            **kwargs
        )
    elif backend == "openai":
        return OpenaiLLM.getDictionaryOutput(
            messages,
            schema,
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
            stop=stop,
            api_key=api_key,
            api_timeout=api_timeout,
            **kwargs
        )
    elif backend == "xai":
        return XaiLLM.getDictionaryOutput(
            messages,
            schema,
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
            stop=stop,
            api_key=api_key,
            api_timeout=api_timeout,
            **kwargs
        )
    return {}

def updateSystemMessage(messages: List[Dict[str, str]], system: str) -> str:
    """
    update system message content in the given message list
    and return the original system message
    """
    original_system = ""
    for i in messages:
        if i.get("role", "") == "system":
            original_system = i.get("content", "")
            i["content"] = system
            break
    return original_system

def addContextToMessages(messages: List[Dict[str, str]], context: str):
    """
    add context to user prompt
    assuming user prompt is placed in the last item of the given message list
    """
    messages[-1] = {"role": "user", "content": getRagPrompt(messages[-1].get("content", ""), context)}
