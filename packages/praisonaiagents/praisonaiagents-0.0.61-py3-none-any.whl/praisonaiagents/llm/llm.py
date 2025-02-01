import logging
import os
import warnings
from typing import Any, Dict, List, Optional, Union, Literal, Callable
from pydantic import BaseModel
import time
import json
from ..main import (
    display_error,
    display_tool_call,
    display_instruction,
    display_interaction,
    display_generating,
    display_self_reflection,
    ReflectionOutput,
)
from rich.console import Console
from rich.live import Live

# TODO: Include in-build tool calling in LLM class
# TODO: Restructure so that duplicate calls are not made (Sync with agent.py)
class LLMContextLengthExceededException(Exception):
    """Raised when LLM context length is exceeded"""
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)

    def _is_context_limit_error(self, error_message: str) -> bool:
        """Check if error is related to context length"""
        context_limit_phrases = [
            "maximum context length",
            "context window is too long",
            "context length exceeded",
            "context_length_exceeded"
        ]
        return any(phrase in error_message.lower() for phrase in context_limit_phrases)

class LLM:
    """
    Easy to use wrapper for language models. Supports multiple providers like OpenAI, 
    Anthropic, and others through LiteLLM.
    """
    
    # Default window sizes for different models (75% of actual to be safe)
    MODEL_WINDOWS = {
        # OpenAI
        "gpt-4": 6144,                    # 8,192 actual
        "gpt-4o": 96000,                  # 128,000 actual
        "gpt-4o-mini": 96000,            # 128,000 actual
        "gpt-4-turbo": 96000,            # 128,000 actual
        "o1-preview": 96000,             # 128,000 actual
        "o1-mini": 96000,                # 128,000 actual
        
        # Anthropic
        "claude-3-5-sonnet": 12288,       # 16,384 actual
        "claude-3-sonnet": 12288,         # 16,384 actual
        "claude-3-opus": 96000,           # 128,000 actual
        "claude-3-haiku": 96000,          # 128,000 actual
        
        # Gemini
        "gemini-2.0-flash": 786432,       # 1,048,576 actual
        "gemini-1.5-pro": 1572864,        # 2,097,152 actual
        "gemini-1.5-flash": 786432,       # 1,048,576 actual
        "gemini-1.5-flash-8b": 786432,    # 1,048,576 actual
        
        # Deepseek
        "deepseek-chat": 96000,           # 128,000 actual
        
        # Groq
        "gemma2-9b-it": 6144,            # 8,192 actual
        "gemma-7b-it": 6144,             # 8,192 actual
        "llama3-70b-8192": 6144,         # 8,192 actual
        "llama3-8b-8192": 6144,          # 8,192 actual
        "mixtral-8x7b-32768": 24576,     # 32,768 actual
        "llama-3.3-70b-versatile": 96000, # 128,000 actual
        "llama-3.3-70b-instruct": 96000,  # 128,000 actual
        
        # Other llama models
        "llama-3.1-70b-versatile": 98304, # 131,072 actual
        "llama-3.1-8b-instant": 98304,    # 131,072 actual
        "llama-3.2-1b-preview": 6144,     # 8,192 actual
        "llama-3.2-3b-preview": 6144,     # 8,192 actual
        "llama-3.2-11b-text-preview": 6144,  # 8,192 actual
        "llama-3.2-90b-text-preview": 6144   # 8,192 actual
    }

    def __init__(
        self,
        model: str,
        timeout: Optional[int] = None,
        temperature: Optional[float] = None,
        top_p: Optional[float] = None,
        n: Optional[int] = None,
        max_tokens: Optional[int] = None,
        presence_penalty: Optional[float] = None,
        frequency_penalty: Optional[float] = None,
        logit_bias: Optional[Dict[int, float]] = None,
        response_format: Optional[Dict[str, Any]] = None,
        seed: Optional[int] = None,
        logprobs: Optional[bool] = None,
        top_logprobs: Optional[int] = None,
        api_version: Optional[str] = None,
        stop_phrases: Optional[Union[str, List[str]]] = None,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        events: List[Any] = [],
        **extra_settings
    ):
        try:
            import litellm
            # Set litellm options globally
            litellm.set_verbose = False
            litellm.success_callback = []
            litellm._async_success_callback = []
            litellm.callbacks = []
            
            verbose = extra_settings.get('verbose', True)
            
            # Only suppress logs if not in debug mode
            if not isinstance(verbose, bool) and verbose >= 10:
                # Enable detailed debug logging
                logging.getLogger("asyncio").setLevel(logging.DEBUG)
                logging.getLogger("selector_events").setLevel(logging.DEBUG)
                logging.getLogger("litellm.utils").setLevel(logging.DEBUG)
                logging.getLogger("litellm.main").setLevel(logging.DEBUG)
                litellm.suppress_debug_messages = False
                litellm.set_verbose = True
            else:
                # Suppress debug logging for normal operation
                logging.getLogger("asyncio").setLevel(logging.WARNING)
                logging.getLogger("selector_events").setLevel(logging.WARNING)
                logging.getLogger("litellm.utils").setLevel(logging.WARNING)
                logging.getLogger("litellm.main").setLevel(logging.WARNING)
                litellm.suppress_debug_messages = True
                litellm._logging._disable_debugging()
                warnings.filterwarnings("ignore", category=RuntimeWarning)
            
        except ImportError:
            raise ImportError(
                "LiteLLM is required but not installed. "
                "Please install with: pip install 'praisonaiagents[llm]'"
            )

        self.model = model
        self.timeout = timeout
        self.temperature = temperature
        self.top_p = top_p
        self.n = n
        self.max_tokens = max_tokens
        self.presence_penalty = presence_penalty
        self.frequency_penalty = frequency_penalty
        self.logit_bias = logit_bias
        self.response_format = response_format
        self.seed = seed
        self.logprobs = logprobs
        self.top_logprobs = top_logprobs
        self.api_version = api_version
        self.stop_phrases = stop_phrases
        self.api_key = api_key
        self.base_url = base_url
        self.events = events
        self.extra_settings = extra_settings
        self.console = Console()
        self.chat_history = []
        self.verbose = verbose
        self.markdown = extra_settings.get('markdown', True)
        self.self_reflect = extra_settings.get('self_reflect', False)
        self.max_reflect = extra_settings.get('max_reflect', 3)
        self.min_reflect = extra_settings.get('min_reflect', 1)
        self.reasoning_steps = extra_settings.get('reasoning_steps', False)
        
        # Enable error dropping for cleaner output
        litellm.drop_params = True
        self._setup_event_tracking(events)

    def get_response(
        self,
        prompt: Union[str, List[Dict]],
        system_prompt: Optional[str] = None,
        chat_history: Optional[List[Dict]] = None,
        temperature: float = 0.2,
        tools: Optional[List[Any]] = None,
        output_json: Optional[BaseModel] = None,
        output_pydantic: Optional[BaseModel] = None,
        verbose: bool = True,
        markdown: bool = True,
        self_reflect: bool = False,
        max_reflect: int = 3,
        min_reflect: int = 1,
        console: Optional[Console] = None,
        agent_name: Optional[str] = None,
        agent_role: Optional[str] = None,
        agent_tools: Optional[List[str]] = None,
        execute_tool_fn: Optional[Callable] = None,
        **kwargs
    ) -> str:
        """Enhanced get_response with all OpenAI-like features"""
        try:
            import litellm
            # This below **kwargs** is passed to .completion() directly. so reasoning_steps has to be popped. OR find alternate best way of handling this.
            reasoning_steps = kwargs.pop('reasoning_steps', self.reasoning_steps) 
            # Disable litellm debug messages
            litellm.set_verbose = False
            
            # Build messages list
            messages = []
            if system_prompt:
                if output_json:
                    system_prompt += f"\nReturn ONLY a JSON object that matches this Pydantic model: {json.dumps(output_json.model_json_schema())}"
                elif output_pydantic:
                    system_prompt += f"\nReturn ONLY a JSON object that matches this Pydantic model: {json.dumps(output_pydantic.model_json_schema())}"
                messages.append({"role": "system", "content": system_prompt})
            
            if chat_history:
                messages.extend(chat_history)

            # Handle prompt modifications for JSON output
            original_prompt = prompt
            if output_json or output_pydantic:
                if isinstance(prompt, str):
                    prompt += "\nReturn ONLY a valid JSON object. No other text or explanation."
                elif isinstance(prompt, list):
                    for item in prompt:
                        if item["type"] == "text":
                            item["text"] += "\nReturn ONLY a valid JSON object. No other text or explanation."
                            break

            # Add prompt to messages
            if isinstance(prompt, list):
                messages.append({"role": "user", "content": prompt})
            else:
                messages.append({"role": "user", "content": prompt})

            start_time = time.time()
            reflection_count = 0

            while True:
                try:
                    if verbose:
                        display_text = prompt
                        if isinstance(prompt, list):
                            display_text = next((item["text"] for item in prompt if item["type"] == "text"), "")
                        
                        if display_text and str(display_text).strip():
                            display_instruction(
                                f"Agent {agent_name} is processing prompt: {display_text}",
                                console=console,
                                agent_name=agent_name,
                                agent_role=agent_role,
                                agent_tools=agent_tools
                            )

                    # Get response from LiteLLM
                    start_time = time.time()

                    # If reasoning_steps is True, do a single non-streaming call
                    if reasoning_steps:
                        resp = litellm.completion(
                            model=self.model,
                            messages=messages,
                            temperature=temperature,
                            stream=False,  # force non-streaming
                            **{k:v for k,v in kwargs.items() if k != 'reasoning_steps'}
                        )
                        reasoning_content = resp["choices"][0]["message"].get("provider_specific_fields", {}).get("reasoning_content")
                        response_text = resp["choices"][0]["message"]["content"]
                        
                        # Optionally display reasoning if present
                        if verbose and reasoning_content:
                            display_interaction(
                                original_prompt,
                                f"Reasoning:\n{reasoning_content}\n\nAnswer:\n{response_text}",
                                markdown=markdown,
                                generation_time=time.time() - start_time,
                                console=console
                            )
                        else:
                            display_interaction(
                                original_prompt,
                                response_text,
                                markdown=markdown,
                                generation_time=time.time() - start_time,
                                console=console
                            )
                    
                    # Otherwise do the existing streaming approach
                    else:
                        if verbose:
                            with Live(display_generating("", start_time), console=console, refresh_per_second=4) as live:
                                response_text = ""
                                for chunk in litellm.completion(
                                    model=self.model,
                                    messages=messages,
                                    temperature=temperature,
                                    stream=True,
                                    **kwargs
                                ):
                                    if chunk and chunk.choices and chunk.choices[0].delta.content:
                                        content = chunk.choices[0].delta.content
                                        response_text += content
                                        live.update(display_generating(response_text, start_time))
                        else:
                            # Non-verbose mode, just collect the response
                            response_text = ""
                            for chunk in litellm.completion(
                                model=self.model,
                                messages=messages,
                                temperature=temperature,
                                stream=True,
                                **kwargs
                            ):
                                if chunk and chunk.choices and chunk.choices[0].delta.content:
                                    response_text += chunk.choices[0].delta.content

                        response_text = response_text.strip()

                    # Get final completion to check for tool calls
                    final_response = litellm.completion(
                        model=self.model,
                        messages=messages,
                        temperature=temperature,
                        stream=False,  # No streaming for tool call check
                        **kwargs
                    )
                    
                    tool_calls = final_response["choices"][0]["message"].get("tool_calls")
                    
                    # Handle tool calls
                    if tool_calls and execute_tool_fn:
                        messages.append({
                            "role": "assistant",
                            "content": response_text,
                            "tool_calls": tool_calls
                        })
                        
                        for tool_call in tool_calls:
                            function_name = tool_call["function"]["name"]
                            arguments = json.loads(tool_call["function"]["arguments"])

                            if verbose:
                                display_tool_call(f"Agent {agent_name} is calling function '{function_name}' with arguments: {arguments}", console=console)

                            tool_result = execute_tool_fn(function_name, arguments)

                            if tool_result:
                                if verbose:
                                    display_tool_call(f"Function '{function_name}' returned: {tool_result}", console=console)
                                messages.append({
                                    "role": "tool",
                                    "tool_call_id": tool_call["id"],
                                    "content": json.dumps(tool_result)
                                })
                            else:
                                messages.append({
                                    "role": "tool",
                                    "tool_call_id": tool_call["id"],
                                    "content": "Function returned an empty output"
                                })

                        # If reasoning_steps is True, do a single non-streaming call
                        if reasoning_steps:
                            resp = litellm.completion(
                                model=self.model,
                                messages=messages,
                                temperature=temperature,
                                stream=False,  # force non-streaming
                                **{k:v for k,v in kwargs.items() if k != 'reasoning_steps'}
                            )
                            reasoning_content = resp["choices"][0]["message"].get("provider_specific_fields", {}).get("reasoning_content")
                            response_text = resp["choices"][0]["message"]["content"]
                            
                            # Optionally display reasoning if present
                            if verbose and reasoning_content:
                                display_interaction(
                                    original_prompt,
                                    f"Reasoning:\n{reasoning_content}\n\nAnswer:\n{response_text}",
                                    markdown=markdown,
                                    generation_time=time.time() - start_time,
                                    console=console
                                )
                            else:
                                display_interaction(
                                    original_prompt,
                                    response_text,
                                    markdown=markdown,
                                    generation_time=time.time() - start_time,
                                    console=console
                                )
                        
                        # Otherwise do the existing streaming approach
                        else:
                            # Get response after tool calls with streaming
                            if verbose:
                                with Live(display_generating("", start_time), console=console, refresh_per_second=4) as live:
                                    response_text = ""
                                    for chunk in litellm.completion(
                                        model=self.model,
                                        messages=messages,
                                        temperature=temperature,
                                        stream=True
                                    ):
                                        if chunk and chunk.choices and chunk.choices[0].delta.content:
                                            content = chunk.choices[0].delta.content
                                            response_text += content
                                            live.update(display_generating(response_text, start_time))
                            else:
                                response_text = ""
                                for chunk in litellm.completion(
                                    model=self.model,
                                    messages=messages,
                                    temperature=temperature,
                                    stream=True
                                ):
                                    if chunk and chunk.choices and chunk.choices[0].delta.content:
                                        response_text += chunk.choices[0].delta.content

                            response_text = response_text.strip()

                    # Handle output formatting
                    if output_json or output_pydantic:
                        self.chat_history.append({"role": "user", "content": original_prompt})
                        self.chat_history.append({"role": "assistant", "content": response_text})
                        if verbose:
                            display_interaction(original_prompt, response_text, markdown=markdown,
                                             generation_time=time.time() - start_time, console=console)
                        return response_text

                    if not self_reflect:
                        if verbose:
                            display_interaction(original_prompt, response_text, markdown=markdown,
                                             generation_time=time.time() - start_time, console=console)
                        # Return reasoning content if reasoning_steps is True
                        if reasoning_steps and reasoning_content:
                            return reasoning_content
                        return response_text

                    # Handle self-reflection
                    reflection_prompt = f"""
Reflect on your previous response: '{response_text}'.
Identify any flaws, improvements, or actions.
Provide a "satisfactory" status ('yes' or 'no').
Output MUST be JSON with 'reflection' and 'satisfactory'.
                    """
                    
                    reflection_messages = messages + [
                        {"role": "assistant", "content": response_text},
                        {"role": "user", "content": reflection_prompt}
                    ]

                    # If reasoning_steps is True, do a single non-streaming call to capture reasoning
                    if reasoning_steps:
                        reflection_resp = litellm.completion(
                            model=self.model,
                            messages=reflection_messages,
                            temperature=temperature,
                            stream=False,  # Force non-streaming
                            response_format={"type": "json_object"},
                            **{k:v for k,v in kwargs.items() if k != 'reasoning_steps'}
                        )
                        # Grab reflection text and optional reasoning
                        reasoning_content = reflection_resp["choices"][0]["message"].get("provider_specific_fields", {}).get("reasoning_content")
                        reflection_text = reflection_resp["choices"][0]["message"]["content"]

                        # Optionally display reasoning if present
                        if verbose and reasoning_content:
                            display_interaction(
                                "Reflection reasoning:",
                                f"{reasoning_content}\n\nReflection result:\n{reflection_text}",
                                markdown=markdown,
                                generation_time=time.time() - start_time,
                                console=console
                            )
                        elif verbose:
                            display_interaction(
                                "Self-reflection (non-streaming):",
                                reflection_text,
                                markdown=markdown,
                                generation_time=time.time() - start_time,
                                console=console
                            )
                    else:
                        # Existing streaming approach
                        if verbose:
                            with Live(display_generating("", start_time), console=console, refresh_per_second=4) as live:
                                reflection_text = ""
                                for chunk in litellm.completion(
                                    model=self.model,
                                    messages=reflection_messages,
                                    temperature=temperature,
                                    stream=True,
                                    response_format={"type": "json_object"},
                                    **{k:v for k,v in kwargs.items() if k != 'reasoning_steps'}
                                ):
                                    if chunk and chunk.choices and chunk.choices[0].delta.content:
                                        content = chunk.choices[0].delta.content
                                        reflection_text += content
                                        live.update(display_generating(reflection_text, start_time))
                        else:
                            reflection_text = ""
                            for chunk in litellm.completion(
                                model=self.model,
                                messages=reflection_messages,
                                temperature=temperature,
                                stream=True,
                                response_format={"type": "json_object"},
                                **{k:v for k,v in kwargs.items() if k != 'reasoning_steps'}
                            ):
                                if chunk and chunk.choices and chunk.choices[0].delta.content:
                                    reflection_text += chunk.choices[0].delta.content

                    try:
                        reflection_data = json.loads(reflection_text)
                        satisfactory = reflection_data.get("satisfactory", "no").lower() == "yes"

                        if verbose:
                            display_self_reflection(
                                f"Agent {agent_name} self reflection: reflection='{reflection_data['reflection']}' satisfactory='{reflection_data['satisfactory']}'",
                                console=console
                            )

                        if satisfactory and reflection_count >= min_reflect - 1:
                            if verbose:
                                display_interaction(prompt, response_text, markdown=markdown,
                                                 generation_time=time.time() - start_time, console=console)
                            return response_text

                        if reflection_count >= max_reflect - 1:
                            if verbose:
                                display_interaction(prompt, response_text, markdown=markdown,
                                                 generation_time=time.time() - start_time, console=console)
                            return response_text

                        reflection_count += 1
                        messages.extend([
                            {"role": "assistant", "content": response_text},
                            {"role": "user", "content": reflection_prompt},
                            {"role": "assistant", "content": reflection_text},
                            {"role": "user", "content": "Now regenerate your response using the reflection you made"}
                        ])
                        continue

                    except json.JSONDecodeError:
                        reflection_count += 1
                        if reflection_count >= max_reflect:
                            return response_text
                        continue

                except Exception as e:
                    display_error(f"Error in LLM response: {str(e)}")
                    return None

        except Exception as error:
            display_error(f"Error in get_response: {str(error)}")
            raise

    async def get_response_async(
        self,
        prompt: Union[str, List[Dict]],
        system_prompt: Optional[str] = None,
        chat_history: Optional[List[Dict]] = None,
        temperature: float = 0.2,
        tools: Optional[List[Any]] = None,
        output_json: Optional[BaseModel] = None,
        output_pydantic: Optional[BaseModel] = None,
        verbose: bool = True,
        markdown: bool = True,
        self_reflect: bool = False,
        max_reflect: int = 3,
        min_reflect: int = 1,
        console: Optional[Console] = None,
        agent_name: Optional[str] = None,
        agent_role: Optional[str] = None,
        agent_tools: Optional[List[str]] = None,
        execute_tool_fn: Optional[Callable] = None,
        **kwargs
    ) -> str:
        """Async version of get_response with identical functionality."""
        try:
            import litellm
            reasoning_steps = kwargs.pop('reasoning_steps', self.reasoning_steps)
            litellm.set_verbose = False

            # Build messages list
            messages = []
            if system_prompt:
                if output_json:
                    system_prompt += f"\nReturn ONLY a JSON object that matches this Pydantic model: {json.dumps(output_json.model_json_schema())}"
                elif output_pydantic:
                    system_prompt += f"\nReturn ONLY a JSON object that matches this Pydantic model: {json.dumps(output_pydantic.model_json_schema())}"
                messages.append({"role": "system", "content": system_prompt})
            
            if chat_history:
                messages.extend(chat_history)

            # Handle prompt modifications for JSON output
            original_prompt = prompt
            if output_json or output_pydantic:
                if isinstance(prompt, str):
                    prompt += "\nReturn ONLY a valid JSON object. No other text or explanation."
                elif isinstance(prompt, list):
                    for item in prompt:
                        if item["type"] == "text":
                            item["text"] += "\nReturn ONLY a valid JSON object. No other text or explanation."
                            break

            # Add prompt to messages
            if isinstance(prompt, list):
                messages.append({"role": "user", "content": prompt})
            else:
                messages.append({"role": "user", "content": prompt})

            start_time = time.time()
            reflection_count = 0

            # Format tools for LiteLLM
            formatted_tools = None
            if tools:
                logging.debug(f"Starting tool formatting for {len(tools)} tools")
                formatted_tools = []
                for tool in tools:
                    logging.debug(f"Processing tool: {tool.__name__ if hasattr(tool, '__name__') else str(tool)}")
                    if hasattr(tool, '__name__'):
                        tool_name = tool.__name__
                        tool_doc = tool.__doc__ or "No description available"
                        # Get function signature
                        import inspect
                        sig = inspect.signature(tool)
                        logging.debug(f"Tool signature: {sig}")
                        params = {}
                        required = []
                        for name, param in sig.parameters.items():
                            logging.debug(f"Processing parameter: {name} with annotation: {param.annotation}")
                            param_type = "string"
                            if param.annotation != inspect.Parameter.empty:
                                if param.annotation == int:
                                    param_type = "integer"
                                elif param.annotation == float:
                                    param_type = "number"
                                elif param.annotation == bool:
                                    param_type = "boolean"
                                elif param.annotation == Dict:
                                    param_type = "object"
                                elif param.annotation == List:
                                    param_type = "array"
                                elif hasattr(param.annotation, "__name__"):
                                    param_type = param.annotation.__name__.lower()
                            params[name] = {"type": param_type}
                            if param.default == inspect.Parameter.empty:
                                required.append(name)
                        
                        logging.debug(f"Generated parameters: {params}")
                        logging.debug(f"Required parameters: {required}")
                        
                        tool_def = {
                            "type": "function",
                            "function": {
                                "name": tool_name,
                                "description": tool_doc,
                                "parameters": {
                                    "type": "object",
                                    "properties": params,
                                    "required": required
                                }
                            }
                        }
                        # Ensure tool definition is JSON serializable
                        try:
                            json.dumps(tool_def)  # Test serialization
                            logging.debug(f"Generated tool definition: {tool_def}")
                            formatted_tools.append(tool_def)
                        except TypeError as e:
                            logging.error(f"Tool definition not JSON serializable: {e}")
                            continue

            # Validate final tools list
            if formatted_tools:
                try:
                    json.dumps(formatted_tools)  # Final serialization check
                    logging.debug(f"Final formatted tools: {json.dumps(formatted_tools, indent=2)}")
                except TypeError as e:
                    logging.error(f"Final tools list not JSON serializable: {e}")
                    formatted_tools = None

            response_text = ""
            if reasoning_steps:
                # Non-streaming call to capture reasoning
                resp = await litellm.acompletion(
                    model=self.model,
                    messages=messages,
                    temperature=temperature,
                    stream=False,  # force non-streaming
                    **{k:v for k,v in kwargs.items() if k != 'reasoning_steps'}
                )
                reasoning_content = resp["choices"][0]["message"].get("provider_specific_fields", {}).get("reasoning_content")
                response_text = resp["choices"][0]["message"]["content"]
                
                if verbose and reasoning_content:
                    display_interaction(
                        "Initial reasoning:",
                        f"Reasoning:\n{reasoning_content}\n\nAnswer:\n{response_text}",
                        markdown=markdown,
                        generation_time=time.time() - start_time,
                        console=console
                    )
                elif verbose:
                    display_interaction(
                        "Initial response:",
                        response_text,
                        markdown=markdown,
                        generation_time=time.time() - start_time,
                        console=console
                    )
            else:
                if verbose:
                    # ----------------------------------------------------
                    # 1) Make the streaming call WITHOUT tools
                    # ----------------------------------------------------
                    async for chunk in await litellm.acompletion(
                        model=self.model,
                        messages=messages,
                        temperature=temperature,
                        stream=True,
                        **kwargs
                    ):
                        if chunk and chunk.choices and chunk.choices[0].delta.content:
                            response_text += chunk.choices[0].delta.content
                            print("\033[K", end="\r")  
                            print(f"Generating... {time.time() - start_time:.1f}s", end="\r")
                else:
                    # Non-verbose streaming call, still no tools
                    async for chunk in await litellm.acompletion(
                        model=self.model,
                        messages=messages,
                        temperature=temperature,
                        stream=True,
                        **kwargs
                    ):
                        if chunk and chunk.choices and chunk.choices[0].delta.content:
                            response_text += chunk.choices[0].delta.content

            response_text = response_text.strip()

            # ----------------------------------------------------
            # 2) If tool calls are needed, do a non-streaming call
            # ----------------------------------------------------
            if tools and execute_tool_fn:
                # Next call with tools if needed
                tool_response = await litellm.acompletion(
                    model=self.model,
                    messages=messages,
                    temperature=temperature,
                    stream=False,
                    tools=formatted_tools,  # We safely pass tools here
                    **{k:v for k,v in kwargs.items() if k != 'reasoning_steps'}
                )
                # handle tool_calls from tool_response as usual...
                tool_calls = tool_response.choices[0].message.get("tool_calls")
                
                if tool_calls:
                    messages.append({
                        "role": "assistant",
                        "content": response_text,
                        "tool_calls": tool_calls
                    })
                    
                    for tool_call in tool_calls:
                        function_name = tool_call.function.name
                        arguments = json.loads(tool_call.function.arguments)

                        if verbose:
                            display_tool_call(f"Agent {agent_name} is calling function '{function_name}' with arguments: {arguments}", console=console)

                        tool_result = await execute_tool_fn(function_name, arguments)

                        if tool_result:
                            if verbose:
                                display_tool_call(f"Function '{function_name}' returned: {tool_result}", console=console)
                            messages.append({
                                "role": "tool",
                                "tool_call_id": tool_call.id,
                                "content": json.dumps(tool_result)
                            })
                        else:
                            messages.append({
                                "role": "tool",
                                "tool_call_id": tool_call.id,
                                "content": "Function returned an empty output"
                            })

                    # Get response after tool calls
                    response_text = ""
                    if reasoning_steps:
                        # Non-streaming call to capture reasoning
                        resp = await litellm.acompletion(
                            model=self.model,
                            messages=messages,
                            temperature=temperature,
                            stream=False,  # force non-streaming
                            tools=formatted_tools,  # Include tools
                            **{k:v for k,v in kwargs.items() if k != 'reasoning_steps'}
                        )
                        reasoning_content = resp["choices"][0]["message"].get("provider_specific_fields", {}).get("reasoning_content")
                        response_text = resp["choices"][0]["message"]["content"]
                        
                        if verbose and reasoning_content:
                            display_interaction(
                                "Tool response reasoning:",
                                f"Reasoning:\n{reasoning_content}\n\nAnswer:\n{response_text}",
                                markdown=markdown,
                                generation_time=time.time() - start_time,
                                console=console
                            )
                        elif verbose:
                            display_interaction(
                                "Tool response:",
                                response_text,
                                markdown=markdown,
                                generation_time=time.time() - start_time,
                                console=console
                            )
                    else:
                        # Get response after tool calls with streaming
                        if verbose:
                            async for chunk in await litellm.acompletion(
                                model=self.model,
                                messages=messages,
                                temperature=temperature,
                                stream=True,
                                tools=formatted_tools,
                                **{k:v for k,v in kwargs.items() if k != 'reasoning_steps'}
                            ):
                                if chunk and chunk.choices and chunk.choices[0].delta.content:
                                    content = chunk.choices[0].delta.content
                                    response_text += content
                                    print("\033[K", end="\r")
                                    print(f"Reflecting... {time.time() - start_time:.1f}s", end="\r")
                        else:
                            response_text = ""
                            for chunk in litellm.completion(
                                model=self.model,
                                messages=messages,
                                temperature=temperature,
                                stream=True,
                                **{k:v for k,v in kwargs.items() if k != 'reasoning_steps'}
                            ):
                                if chunk and chunk.choices and chunk.choices[0].delta.content:
                                    response_text += chunk.choices[0].delta.content

                    response_text = response_text.strip()

            # Handle output formatting
            if output_json or output_pydantic:
                self.chat_history.append({"role": "user", "content": original_prompt})
                self.chat_history.append({"role": "assistant", "content": response_text})
                if verbose:
                    display_interaction(original_prompt, response_text, markdown=markdown,
                                     generation_time=time.time() - start_time, console=console)
                return response_text

            if not self_reflect:
                if verbose:
                    display_interaction(original_prompt, response_text, markdown=markdown,
                                     generation_time=time.time() - start_time, console=console)
                # Return reasoning content if reasoning_steps is True
                if reasoning_steps and reasoning_content:
                    return reasoning_content
                return response_text

            # Handle self-reflection
            reflection_prompt = f"""
Reflect on your previous response: '{response_text}'.
Identify any flaws, improvements, or actions.
Provide a "satisfactory" status ('yes' or 'no').
Output MUST be JSON with 'reflection' and 'satisfactory'.
            """
            
            reflection_messages = messages + [
                {"role": "assistant", "content": response_text},
                {"role": "user", "content": reflection_prompt}
            ]

            # If reasoning_steps is True, do a single non-streaming call to capture reasoning
            if reasoning_steps:
                reflection_resp = litellm.completion(
                    model=self.model,
                    messages=reflection_messages,
                    temperature=temperature,
                    stream=False,  # Force non-streaming
                    response_format={"type": "json_object"},
                    **{k:v for k,v in kwargs.items() if k != 'reasoning_steps'}
                )
                # Grab reflection text and optional reasoning
                reasoning_content = reflection_resp["choices"][0]["message"].get("provider_specific_fields", {}).get("reasoning_content")
                reflection_text = reflection_resp["choices"][0]["message"]["content"]

                # Optionally display reasoning if present
                if verbose and reasoning_content:
                    display_interaction(
                        "Reflection reasoning:",
                        f"{reasoning_content}\n\nReflection result:\n{reflection_text}",
                        markdown=markdown,
                        generation_time=time.time() - start_time,
                        console=console
                    )
                elif verbose:
                    display_interaction(
                        "Self-reflection (non-streaming):",
                        reflection_text,
                        markdown=markdown,
                        generation_time=time.time() - start_time,
                        console=console
                    )
            else:
                # Existing streaming approach
                if verbose:
                    with Live(display_generating("", start_time), console=console, refresh_per_second=4) as live:
                        reflection_text = ""
                        for chunk in litellm.completion(
                            model=self.model,
                            messages=reflection_messages,
                            temperature=temperature,
                            stream=True,
                            response_format={"type": "json_object"},
                            **{k:v for k,v in kwargs.items() if k != 'reasoning_steps'}
                        ):
                            if chunk and chunk.choices and chunk.choices[0].delta.content:
                                content = chunk.choices[0].delta.content
                                reflection_text += content
                                live.update(display_generating(reflection_text, start_time))
                else:
                    reflection_text = ""
                    for chunk in litellm.completion(
                        model=self.model,
                        messages=reflection_messages,
                        temperature=temperature,
                        stream=True,
                        response_format={"type": "json_object"},
                        **{k:v for k,v in kwargs.items() if k != 'reasoning_steps'}
                    ):
                        if chunk and chunk.choices and chunk.choices[0].delta.content:
                            reflection_text += chunk.choices[0].delta.content

            while True:  # Add loop for reflection handling
                try:
                    reflection_data = json.loads(reflection_text)
                    satisfactory = reflection_data.get("satisfactory", "no").lower() == "yes"

                    if verbose:
                        display_self_reflection(
                            f"Agent {agent_name} self reflection: reflection='{reflection_data['reflection']}' satisfactory='{reflection_data['satisfactory']}'",
                            console=console
                        )

                    if satisfactory and reflection_count >= min_reflect - 1:
                        if verbose:
                            display_interaction(prompt, response_text, markdown=markdown,
                                             generation_time=time.time() - start_time, console=console)
                        return response_text

                    if reflection_count >= max_reflect - 1:
                        if verbose:
                            display_interaction(prompt, response_text, markdown=markdown,
                                             generation_time=time.time() - start_time, console=console)
                        return response_text

                    reflection_count += 1
                    messages.extend([
                        {"role": "assistant", "content": response_text},
                        {"role": "user", "content": reflection_prompt},
                        {"role": "assistant", "content": reflection_text},
                        {"role": "user", "content": "Now regenerate your response using the reflection you made"}
                    ])
                    continue  # Now properly in a loop

                except json.JSONDecodeError:
                    reflection_count += 1
                    if reflection_count >= max_reflect:
                        return response_text
                    continue  # Now properly in a loop
            
        except Exception as error:
            if LLMContextLengthExceededException(str(error))._is_context_limit_error(str(error)):
                raise LLMContextLengthExceededException(str(error))
            display_error(f"Error in get_response_async: {str(error)}")
            raise

    def can_use_tools(self) -> bool:
        """Check if this model can use tool functions"""
        try:
            import litellm
            allowed_params = litellm.get_supported_openai_params(model=self.model)
            return "response_format" in allowed_params
        except ImportError:
            raise ImportError(
                "LiteLLM is required but not installed. "
                "Please install it with: pip install 'praisonaiagents[llm]'"
            )
        except:
            return False

    def can_use_stop_words(self) -> bool:
        """Check if this model supports stop words"""
        try:
            import litellm
            allowed_params = litellm.get_supported_openai_params(model=self.model)
            return "stop" in allowed_params
        except ImportError:
            raise ImportError(
                "LiteLLM is required but not installed. "
                "Please install it with: pip install 'praisonaiagents[llm]'"
            )
        except:
            return False

    def get_context_size(self) -> int:
        """Get safe input size limit for this model"""
        for model_prefix, size in self.MODEL_WINDOWS.items():
            if self.model.startswith(model_prefix):
                return size
        return 4000  # Safe default

    def _setup_event_tracking(self, events: List[Any]) -> None:
        """Setup callback functions for tracking model usage"""
        try:
            import litellm
        except ImportError:
            raise ImportError(
                "LiteLLM is required but not installed. "
                "Please install it with: pip install 'praisonaiagents[llm]'"
            )

        event_types = [type(event) for event in events]
        
        # Remove old events of same type
        for event in litellm.success_callback[:]:
            if type(event) in event_types:
                litellm.success_callback.remove(event)
                
        for event in litellm._async_success_callback[:]:
            if type(event) in event_types:
                litellm._async_success_callback.remove(event)
                
        litellm.callbacks = events

    # Response without tool calls
    def response(
        self,
        prompt: Union[str, List[Dict]],
        system_prompt: Optional[str] = None,
        temperature: float = 0.2,
        stream: bool = True,
        verbose: bool = True,
        markdown: bool = True,
        console: Optional[Console] = None,
        **kwargs
    ) -> str:
        """Simple function to get model response without tool calls or complex features"""
        try:
            import litellm
            import logging
            logger = logging.getLogger(__name__)
            
            litellm.set_verbose = False
            start_time = time.time()
            
            logger.debug("Using synchronous response function")
            
            # Build messages list
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            
            # Add prompt to messages
            if isinstance(prompt, list):
                messages.append({"role": "user", "content": prompt})
            else:
                messages.append({"role": "user", "content": prompt})

            # Get response from LiteLLM
            if stream:
                response_text = ""
                if verbose:
                    with Live(display_generating("", start_time), console=console or self.console, refresh_per_second=4) as live:
                        for chunk in litellm.completion(
                            model=self.model,
                            messages=messages,
                            temperature=temperature,
                            stream=True,
                            **kwargs
                        ):
                            if chunk and chunk.choices and chunk.choices[0].delta.content:
                                content = chunk.choices[0].delta.content
                                response_text += content
                                live.update(display_generating(response_text, start_time))
                else:
                    for chunk in litellm.completion(
                        model=self.model,
                        messages=messages,
                        temperature=temperature,
                        stream=True,
                        **kwargs
                    ):
                        if chunk and chunk.choices and chunk.choices[0].delta.content:
                            response_text += chunk.choices[0].delta.content
            else:
                response = litellm.completion(
                    model=self.model,
                    messages=messages,
                    temperature=temperature,
                    stream=False,
                    **kwargs
                )
                response_text = response.choices[0].message.content.strip()

            if verbose:
                display_interaction(
                    prompt if isinstance(prompt, str) else prompt[0].get("text", ""),
                    response_text,
                    markdown=markdown,
                    generation_time=time.time() - start_time,
                    console=console or self.console
                )
            
            return response_text.strip()

        except Exception as error:
            display_error(f"Error in response: {str(error)}")
            raise

    # Async version of response function. Response without tool calls
    async def aresponse(
        self,
        prompt: Union[str, List[Dict]],
        system_prompt: Optional[str] = None,
        temperature: float = 0.2,
        stream: bool = True,
        verbose: bool = True,
        markdown: bool = True,
        console: Optional[Console] = None,
        **kwargs
    ) -> str:
        """Async version of response function"""
        try:
            import litellm
            import logging
            logger = logging.getLogger(__name__)
            
            litellm.set_verbose = False
            start_time = time.time()
            
            logger.debug("Using asynchronous response function")
            
            # Build messages list
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            
            # Add prompt to messages
            if isinstance(prompt, list):
                messages.append({"role": "user", "content": prompt})
            else:
                messages.append({"role": "user", "content": prompt})

            # Get response from LiteLLM
            if stream:
                response_text = ""
                if verbose:
                    with Live(display_generating("", start_time), console=console or self.console, refresh_per_second=4) as live:
                        async for chunk in await litellm.acompletion(
                            model=self.model,
                            messages=messages,
                            temperature=temperature,
                            stream=True,
                            **kwargs
                        ):
                            if chunk and chunk.choices and chunk.choices[0].delta.content:
                                content = chunk.choices[0].delta.content
                                response_text += content
                                live.update(display_generating(response_text, start_time))
                else:
                    async for chunk in await litellm.acompletion(
                        model=self.model,
                        messages=messages,
                        temperature=temperature,
                        stream=True,
                        **kwargs
                    ):
                        if chunk and chunk.choices and chunk.choices[0].delta.content:
                            response_text += chunk.choices[0].delta.content
            else:
                response = await litellm.acompletion(
                    model=self.model,
                    messages=messages,
                    temperature=temperature,
                    stream=False,
                    **kwargs
                )
                response_text = response.choices[0].message.content.strip()

            if verbose:
                display_interaction(
                    prompt if isinstance(prompt, str) else prompt[0].get("text", ""),
                    response_text,
                    markdown=markdown,
                    generation_time=time.time() - start_time,
                    console=console or self.console
                )
            
            return response_text.strip()

        except Exception as error:
            display_error(f"Error in response_async: {str(error)}")
            raise