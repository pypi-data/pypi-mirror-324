from fastapi import FastAPI, Request, BackgroundTasks
from fastapi.responses import JSONResponse
import logging
from computer_use.loop import sampling_loop, ToolResult, APIProvider, PROVIDER_TO_DEFAULT_MODEL_NAME
from computer_use.tools.computer import ComputerTool, Action
import os
from pydantic import BaseModel
from typing import Optional, List, Dict, Any, Tuple
from fastapi.middleware.cors import CORSMiddleware
from sse_starlette.sse import EventSourceResponse
import asyncio
import json
import uuid
import signal
from datetime import datetime
import copy

import uvicorn

# Define the log directory
LOG_DIR = "/home/computeruse/logs"
os.makedirs(LOG_DIR, exist_ok=True)  # Ensure the directory exists

# Configure logging to write to a file in LOG_DIR with timestamp
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s:%(name)s:%(message)s',
    handlers=[
        logging.FileHandler(f"{LOG_DIR}/{timestamp}.log"),  # Log with timestamp
        logging.StreamHandler(),
    ]
)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
# logger.propagate = False

# Set logging level to WARNING for other modules to reduce verbosity
logging.getLogger('llm_provider').setLevel(logging.WARNING)
logging.getLogger('httpx').setLevel(logging.WARNING)
logging.getLogger('httpcore').setLevel(logging.WARNING)

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure with your frontend's URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the ComputerTool instance
computer_tool = ComputerTool()

# Store messages and tasks per conversation
conversations: Dict[str, Any] = {}

# Define a single global conversation ID
GLOBAL_CONVERSATION_ID = 'global_conversation'

# Get provider authentication from environment
API_KEY = os.getenv("API_KEY", "")  # Default to empty string instead of None
if not API_KEY:
    raise ValueError("API_KEY environment variable is required")

reset_event = asyncio.Event()  # Initialize the reset event

# Global list to keep track of background tasks
background_tasks = []

class ChatRequest(BaseModel):
    message: str
    only_n_most_recent_images: Optional[int] = None
    num_uncached_messages: Optional[int] = 5
    exclude_images: Optional[bool] = False
    messages_to_include: Optional[int] = None
    tool_choice: Optional[dict] = {"type": "auto"}

@app.post("/api/chat")
async def chat(request: ChatRequest):
    """
    Handle incoming chat messages and manage the conversation loop.

    **Parameters:**

    - `message`: The user's message.
    - `only_n_most_recent_images`: Limit the number of images to include.
    - `num_uncached_messages`: Number of recent messages not to cache.
    - `exclude_images`: If `True`, images are excluded from messages.
    - `messages_to_include`: If set, only the last `messages_to_include` messages are sent to the API.
    """
    user_message = request.message
    logger.info(f"Received message: {user_message} with conversation_id: {GLOBAL_CONVERSATION_ID}")

    # Initialize conversation without examples (since they are in the system prompt)
    if GLOBAL_CONVERSATION_ID not in conversations:
        conversations[GLOBAL_CONVERSATION_ID] = {
            'messages': [],  # Start with an empty message list
            'task': None,
            'message_queue': asyncio.Queue(),
            'reset_event': asyncio.Event()
        }

    conversation = conversations[GLOBAL_CONVERSATION_ID]
    messages = conversation['messages']

    # Append the user's message to the messages list
    messages.append({
        "role": "user",
        "content": [{"type": "text", "text": user_message}]
    })

    # Define async callbacks
    async def output_callback(x):
        await conversation['message_queue'].put({"type": "assistant", "content": x})

    async def tool_output_callback(result, tool_use_id):
        result_dict = vars(result).copy()
        result_dict.pop('base64_image', None)
        await conversation['message_queue'].put({
            "type": "tool_usage",
            "content": {
                "result": result_dict,
                "tool_use_id": tool_use_id
            }
        })

    # Cancel any existing sampling loop task for this conversation
    if conversation['task'] and not conversation['task'].done():
        conversation['task'].cancel()
        try:
            await conversation['task']
        except asyncio.CancelledError:
            logger.info("Previous sampling loop task cancelled.")

    # Extract cache configuration from request or set defaults
    only_n_most_recent_images = request.only_n_most_recent_images or 10
    num_uncached_messages = request.num_uncached_messages or 5
    exclude_images = request.exclude_images or False
    messages_to_include = request.messages_to_include

    # Extract tool_choice from request or set default
    tool_choice = request.tool_choice or {"type": "auto"}

    # Start a new sampling loop task
    task = asyncio.create_task(
        sampling_loop(
            system_prompt_suffix="",
            model=PROVIDER_TO_DEFAULT_MODEL_NAME[APIProvider.DEFAULT],
            provider=APIProvider.DEFAULT,
            messages=messages,
            api_key=API_KEY,
            only_n_most_recent_images=only_n_most_recent_images,
            num_uncached_messages=num_uncached_messages,
            exclude_images=exclude_images,
            messages_to_include=messages_to_include,
            output_callback=output_callback,
            tool_output_callback=tool_output_callback,
            api_response_callback=lambda request, response, exception: None,
            reset_event=conversation['reset_event'],
            tool_choice=tool_choice,
        )
    )

    # Update the task reference
    conversation['task'] = task

    return {"conversation_id": GLOBAL_CONVERSATION_ID}

@app.get("/api/chat/stream")
async def chat_stream():
    conversation = conversations.get(GLOBAL_CONVERSATION_ID)
    if not conversation:
        return JSONResponse(content={"error": "No active conversation"}, status_code=400)

    message_queue = conversation['message_queue']

    async def event_generator():
        try:
            while True:
                message = await message_queue.get()
                yield json.dumps(message) + "\n\n"
        except asyncio.CancelledError:
            pass
        except Exception as e:
            logger.error(f"Error in message queue: {str(e)}")
            yield json.dumps({'error': str(e)}) + "\n\n"

    return EventSourceResponse(event_generator())

@app.post("/api/reset")
async def reset():
    conversation = conversations.get(GLOBAL_CONVERSATION_ID)
    if not conversation:
        return JSONResponse(content={"status": "No active conversation to reset"}, status_code=200)

    # Cancel the sampling loop task
    if conversation['task'] and not conversation['task'].done():
        conversation['task'].cancel()
        try:
            await conversation['task']
        except asyncio.CancelledError:
            logger.info("Sampling loop task cancelled.")

    # Clear messages and reset events
    conversation['messages'].clear()
    conversation['reset_event'].set()

    # Reset the desktop environment
    await computer_tool.reset_desktop()

    return JSONResponse(content={"status": "Reset initiated"}, status_code=200)

class ComputerActionRequest(BaseModel):
    action: Action
    text: Optional[str] = None
    coordinate: Optional[Tuple[int, int]] = None

@app.post("/api/computer/action")
async def computer_action(request: ComputerActionRequest):
    try:
        # Validate action
        valid_actions = [
            "key", "type", "mouse_move", "left_click", "left_click_drag",
            "right_click", "middle_click", "double_click", "screenshot",
            "cursor_position"
        ]
        if request.action not in valid_actions:
            return JSONResponse(content={"error": "Invalid action"}, status_code=400)

        # Call the computer tool with provided parameters
        result = await computer_tool(
            action=request.action,
            text=request.text,
            coordinate=request.coordinate
        )

        response_content = {}

        if result.output:
            response_content["output"] = result.output

        if result.error:
            response_content["error"] = result.error
            logger.error(f"Error in computer action: {result.error}")

        if result.base64_image:
            response_content["base64_image"] = result.base64_image

        return JSONResponse(content=response_content)

    except Exception as e:
        logger.error(f"Error in computer action endpoint: {str(e)}")
        return JSONResponse(content={"error": str(e)}, status_code=500)

if __name__ == "__main__":
    print("Starting server...")
    uvicorn.run(app, host="0.0.0.0", port=5001)
