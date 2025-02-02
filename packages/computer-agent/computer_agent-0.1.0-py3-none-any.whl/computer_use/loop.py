"""
Agentic sampling loop
"""

import platform
from collections.abc import Callable
from datetime import datetime
from enum import StrEnum
from typing import Any, cast
import logging
import copy
import asyncio

import httpx
from anthropic import (
    Anthropic,
    AnthropicBedrock,
    AnthropicVertex,
    APIError,
    APIResponseValidationError,
    APIStatusError,
)
from anthropic.types.beta import (
    BetaCacheControlEphemeralParam,
    BetaContentBlockParam,
    BetaImageBlockParam,
    BetaMessage,
    BetaMessageParam,
    BetaTextBlock,
    BetaTextBlockParam,
    BetaToolResultBlockParam,
    BetaToolUseBlockParam,
)

from .tools import BashTool, ComputerTool, EditTool, ToolCollection, ToolResult
from .prompt import SYSTEM_PROMPT

COMPUTER_USE_BETA_FLAG = "computer-use-2024-10-22"
PROMPT_CACHING_BETA_FLAG = "prompt-caching-2024-07-31"

# Configure logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

class APIProvider(StrEnum):
    ANTHROPIC = "anthropic"
    DEEPSEEK = "deepseek"

PROVIDER_TO_DEFAULT_MODEL_NAME: dict[APIProvider, str] = {
    APIProvider.ANTHROPIC: "claude-3-5-sonnet-20241022",
    APIProvider.DEEPSEEK: "deepseek-r1-zero",
}


async def sampling_loop(
    *,
    model: str,
    provider: APIProvider,
    system_prompt_suffix: str,
    messages: list[BetaMessageParam],
    output_callback: Callable[[BetaContentBlockParam], Any],
    tool_output_callback: Callable[[ToolResult, str], None],
    api_response_callback: Callable[
        [httpx.Request, httpx.Response | object | None, Exception | None], None
    ],
    api_key: str,
    reset_event: asyncio.Event,
    only_n_most_recent_images: int | None = None,
    max_tokens: int = 8096,
    num_uncached_messages: int = 5,  # Number of recent messages not to cache
    exclude_images: bool = False,
    messages_to_include: int | None = None,
    tool_choice: dict = {"type": "auto"},  # New parameter
):
    """
    Agentic sampling loop for the assistant/tool interaction of computer use.

    This function manages the conversation loop between the assistant and the user,
    including processing tool uses and handling prompt caching.

    **Caching Strategy Diagram:**

    We segment the conversation into cached and uncached messages to optimize performance.
    ```
    |-- System Prompt & Tools ----------------|
                                              ↑
                                   Cache Breakpoint (after system prompt)
    |-- Older Messages ------------|          |
                                              ↑
                                   Cache Breakpoint (before recent messages)
    |-- Recent Message N -----------|   <-- Latest messages (not cached)
    |-- Recent Message N-1 ---------|
    |-- ... ------------------------|
    ```

    - Messages before the cache breakpoint are cached.
    - The latest `num_uncached_messages` are not cached to ensure up-to-date context.

    **Parameters:**

    - `num_uncached_messages`: Number of recent messages not to cache.
    - `exclude_images`: If `True`, images are excluded from messages to reduce token usage.
    - `messages_to_include`: If set, only the last `messages_to_include` messages are sent to the API.
    """
    # Add debug logging at key points
    logger.info(f"Starting sampling loop with model: {model}, provider: {provider}")

    tool_collection = ToolCollection(
        ComputerTool(),
        BashTool(),
        EditTool(),
    )
    system = BetaTextBlockParam(
        type="text",
        text=f"{SYSTEM_PROMPT}",
    )

    initial_messages = messages.copy()  # Store initial messages
    
    logger.info(f"Here are the initial messages: {initial_messages}")

    try:
        while True:
            if reset_event.is_set():
                messages = initial_messages.copy()  # Reset to initial messages
                reset_event.clear()
                continue  # Restart the loop

            enable_prompt_caching = True
            betas = [COMPUTER_USE_BETA_FLAG]
            image_truncation_threshold = 10

            client = Anthropic(api_key=api_key)

            # Use a deep copy to prevent modifying the original messages
            messages_to_send = copy.deepcopy(messages[-messages_to_include:] if messages_to_include is not None else messages)

            # Optionally exclude images from messages
            if exclude_images:
                _exclude_images(messages_to_send)

            if enable_prompt_caching:
                betas.append(PROMPT_CACHING_BETA_FLAG)
                _inject_prompt_caching(messages_to_send, num_uncached_messages=num_uncached_messages)

                # Apply cache_control to the system prompt if not already set
                if "cache_control" not in system:
                    system["cache_control"] = {"type": "ephemeral"}

            if not exclude_images and only_n_most_recent_images is not None:
                _maybe_filter_to_n_most_recent_images(
                    messages_to_send,
                    only_n_most_recent_images,
                    min_removal_threshold=image_truncation_threshold,
                )

            # Call the API using with_raw_response
            try:
                # logger.info("Making API call to Anthropic API.")
                # logger.info(f"Sending messages: {messages_to_send}")
                logger.info(f"New API call and Tool choice: {tool_choice}")
                raw_response = client.beta.messages.with_raw_response.create(
                    max_tokens=max_tokens,
                    messages=messages_to_send,
                    model=model,
                    system=[system],
                    tools=tool_collection.to_params(),
                    betas=betas,
                    tool_choice=tool_choice,  # Pass the tool_choice parameter
                )
                logger.info("API call completed successfully.")
                logger.debug(f"Raw API response: {raw_response.http_response}")
                logger.debug(f"Response content: {raw_response.parse()}")
            except (APIStatusError, APIResponseValidationError) as e:
                logger.error(f"API error occurred: {str(e)}")
                await api_response_callback(e.request, e.response, e)
                return messages
            except APIError as e:
                logger.error(f"API error occurred: {str(e)}")
                await api_response_callback(e.request, e.body, e)
                return messages
            except Exception as e:
                logger.error(f"An unexpected exception occurred: {str(e)}")
                return messages

            # Get the parsed response
            response = raw_response.parse()

            # Log token usage from response
            if response.usage:
                logger.info(f"Token usage: {response.usage}")

            response_params = _response_to_params(response)
            assistant_message = {
                "role": "assistant",
                "content": response_params,
            }

            messages.append(assistant_message)

            # Initialize tool_result_content
            tool_result_content: list[BetaToolResultBlockParam] = []

            # Process the assistant's response and handle tool uses
            for content_block in response_params:
                await output_callback(content_block)

                if content_block["type"] == "tool_use":
                    # Run the tool
                    result = await tool_collection.run(
                        name=content_block["name"],
                        tool_input=cast(dict[str, Any], content_block["input"]),
                    )

                    # Prepare tool result content
                    tool_result = _make_api_tool_result(result, content_block["id"])

                    # Append the tool result to tool_result_content
                    tool_result_content.append(tool_result)

                    # **Send the tool result back through the tool_output_callback**
                    await tool_output_callback(result, content_block["id"])

            if tool_result_content:
                # **Ensure the user's message starts with the tool_result blocks**
                messages.append({
                    "role": "user",
                    "content": tool_result_content + [
                        # You can add additional user content here if needed
                    ]
                })
            else:
                break

            # Add state logging in main loop
            logger.info(f"Current message count: {len(messages)}")
            logger.debug(f"Last message: {messages[-1] if messages else None}")

            # Check for cancellation
            await asyncio.sleep(0)
    except asyncio.CancelledError:
        logger.info("Sampling loop cancelled.")
        # Perform any necessary cleanup here
        return

    logger.info("Final conversation messages:")
    for msg in messages:
        logger.info(msg)

    # After receiving the assistant's response
    logger.info("Assistant response:")
    logger.info(assistant_message)

    return messages


def _maybe_filter_to_n_most_recent_images(
    messages: list[BetaMessageParam],
    images_to_keep: int | None,
    min_removal_threshold: int,
):
    """
    With the assumption that images are screenshots that are of diminishing value as
    the conversation progresses, remove all but the final `images_to_keep` tool_result
    images in place, with a chunk of min_removal_threshold to reduce the amount we
    break the implicit prompt cache.
    """
    if images_to_keep is None:
        return messages

    # Now, we can choose to keep all images if desired
    if images_to_keep == -1:
        logger.info("Keeping all images in the cache.")
        return messages

    tool_result_blocks = cast(
        list[BetaToolResultBlockParam],
        [
            item
            for message in messages
            for item in (
                message["content"] if isinstance(message["content"], list) else []
            )
            if isinstance(item, dict) and item.get("type") == "tool_result"
        ],
    )

    total_images = sum(
        1
        for tool_result in tool_result_blocks
        for content in tool_result.get("content", [])
        if isinstance(content, dict) and content.get("type") == "image"
    )

    images_to_remove = total_images - images_to_keep
    # for better cache behavior, we want to remove in chunks
    images_to_remove -= images_to_remove % min_removal_threshold

    for tool_result in tool_result_blocks:
        if isinstance(tool_result.get("content"), list):
            new_content = []
            for content in tool_result.get("content", []):
                if isinstance(content, dict) and content.get("type") == "image":
                    if images_to_remove > 0:
                        images_to_remove -= 1
                        continue
                new_content.append(content)
            tool_result["content"] = new_content


def _response_to_params(
    response: BetaMessage,
) -> list[BetaTextBlockParam | BetaToolUseBlockParam]:
    res: list[BetaTextBlockParam | BetaToolUseBlockParam] = []
    for block in response.content:
        if isinstance(block, BetaTextBlock):
            res.append({"type": "text", "text": block.text})
        else:
            res.append(cast(BetaToolUseBlockParam, block.model_dump()))
    return res


def _inject_prompt_caching(messages: list[BetaMessageParam], num_uncached_messages: int = 3):
    """
    Ensure that the total number of `cache_control` blocks does not exceed 4.
    
    **Steps:**

    1. **Clear Existing `cache_control` Annotations:** Remove any existing `cache_control` from all messages.
    2. **Apply `cache_control` to the System Prompt:** Counts as one block.
    3. **Apply `cache_control` to the First Content Block of Earliest Messages:** Until you reach the limit.

    **Parameters:**

    - `messages`: The list of messages to process.
    - `num_uncached_messages`: The number of recent messages not to cache.
    """
    logger.info("Applying cache_control with a maximum of 4 blocks.")

    # Clear existing cache_control annotations
    for message in messages:
        if isinstance(message["content"], list):
            for block in message["content"]:
                block.pop("cache_control", None)

    # Apply cache_control to messages strategically
    cache_control_blocks = 1  # Account for system prompt cache_control
    message_count = len(messages)
    
    for index, message in enumerate(messages):
        if cache_control_blocks >= 4:
            break  # Do not exceed the maximum number of cache_control blocks

        if index < message_count - num_uncached_messages:
            if isinstance(message["content"], list) and len(message["content"]) > 0:
                # Apply cache_control to the first content block of this message
                block = message["content"][0]
                if "cache_control" not in block:
                    block["cache_control"] = {"type": "ephemeral"}
                    cache_control_blocks += 1
        else:
            # Recent messages; ensure cache_control is not set
            if isinstance(message["content"], list):
                for block in message["content"]:
                    block.pop("cache_control", None)


def _make_api_tool_result(
    result: ToolResult, tool_use_id: str
) -> BetaToolResultBlockParam:
    """Convert an agent ToolResult to an API ToolResultBlockParam."""
    tool_result_content: list[BetaTextBlockParam | BetaImageBlockParam] | str = []
    is_error = False
    if result.error:
        is_error = True
        tool_result_content = _maybe_prepend_system_tool_result(result, result.error)
    else:
        if result.output:
            tool_result_content.append(
                {
                    "type": "text",
                    "text": _maybe_prepend_system_tool_result(result, result.output),
                }
            )
        if result.base64_image:
            tool_result_content.append(
                {
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": "image/png",
                        "data": result.base64_image,
                    },
                }
            )
    return {
        "type": "tool_result",
        "content": tool_result_content,
        "tool_use_id": tool_use_id,
        "is_error": is_error,
    }


def _maybe_prepend_system_tool_result(result: ToolResult, result_text: str):
    if result.system:
        result_text = f"<system>{result.system}</system>\n{result_text}"
    return result_text

def _exclude_images(messages: list[BetaMessageParam]):
    """
    Exclude images from messages to reduce message size.

    **Purpose:**

    Images (e.g., screenshots) can be large and increase token usage. Excluding them can improve performance.

    **Parameters:**

    - `messages`: The list of messages to process.
    """
    for message in messages:
        if isinstance(message['content'], list):
            message['content'] = [
                block for block in message['content']
                if not (isinstance(block, dict) and block.get('type') == 'image')
            ]

            message['content'] = [
                block for block in message['content']
                if not (isinstance(block, dict) and block.get('type') == 'image')
            ]

