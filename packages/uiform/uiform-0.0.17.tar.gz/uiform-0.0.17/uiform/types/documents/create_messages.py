from pydantic import BaseModel, Field, model_validator
from typing import cast, Iterable, Optional, Self, TypedDict, Literal, Union, List, Any

import base64
import PIL.Image
import requests
import logging
from io import BytesIO

from ..modalities import Modality
from ..._utils.ai_model import find_provider_from_model
from ..ai_model import AIProvider
from .image_settings import ImageSettings
from ..mime import MIMEData

from openai.types.chat.chat_completion_message_param import ChatCompletionMessageParam
from openai.types.chat.chat_completion_content_part_param import ChatCompletionContentPartParam
from openai.types.chat.chat_completion_content_part_text_param import ChatCompletionContentPartTextParam
from openai.types.chat.chat_completion_content_part_image_param import ChatCompletionContentPartImageParam
from openai.types.chat.chat_completion_content_part_input_audio_param import ChatCompletionContentPartInputAudioParam

from google.generativeai.types import content_types  # type: ignore
from google.generativeai.types import generation_types

from anthropic.types.message_param import MessageParam
from anthropic.types.content_block import ContentBlock
from anthropic.types.text_block_param import TextBlockParam
from anthropic.types.image_block_param import ImageBlockParam, Source
from anthropic.types.tool_use_block_param import ToolUseBlockParam
from anthropic.types.tool_result_block_param import ToolResultBlockParam
#from anthropic._types import NotGiven, NOT_GIVEN

BlockUnion = Union[TextBlockParam, ImageBlockParam, ToolUseBlockParam, ToolResultBlockParam, ContentBlock]
ContentBlockAnthropicUnion = Union[str, Iterable[BlockUnion]]
MediaType = Literal["image/jpeg", "image/png", "image/gif", "image/webp"]

class ChatCompletionUiformMessage(TypedDict):  # homemade replacement for ChatCompletionMessageParam because iterable messes the serialization with pydantic
    role: Literal['user', 'system', 'assistant']
    content : Union[str, list[ChatCompletionContentPartParam]]

def separate_messages(messages: list[ChatCompletionUiformMessage]) -> tuple[Optional[ChatCompletionUiformMessage], list[ChatCompletionUiformMessage], list[ChatCompletionUiformMessage]]:
    """
    Separates messages into system, user and assistant messages.

    Args:
        messages: List of chat messages containing system, user and assistant messages

    Returns:
        Tuple containing:
        - The system message if present, otherwise None
        - List of user messages
        - List of assistant messages
    """
    system_message = None
    user_messages = []
    assistant_messages = []

    for message in messages:
        if message["role"] == "system":
            system_message = message
        elif message["role"] == "user":
            user_messages.append(message)
        elif message["role"] == "assistant":
            assistant_messages.append(message)

    return system_message, user_messages, assistant_messages

def convert_to_google_genai_format(
    messages: List[ChatCompletionUiformMessage]
) -> content_types.ContentsType:
    """
    Converts a list of ChatCompletionUiFormMessage to a format compatible with the google.genai SDK.


    Example:
        ```python
        import google.generativeai as genai
        
        # Configure the Gemini client
        genai.configure(api_key=os.environ["GEMINI_API_KEY"])
        
        # Initialize the model
        model = genai.GenerativeModel("gemini-2.0-flash")
        
        # Get messages in Gemini format
        gemini_messages = document_message.gemini_messages
        
        # Generate a response
        ```

    Args:
        messages (List[ChatCompletionUiformMessage]): List of chat messages.

    Returns:
        List[Union[Dict[str, str], str]]: A list of formatted inputs for the google.genai SDK.
    """

    formatted_inputs: content_types.ContentsType = []
    
    for message in messages:
        if isinstance(message['content'], str):
            # Direct string content is treated as the prompt for the SDK
            formatted_inputs.append(message['content']) # type: ignore
        elif isinstance(message['content'], list):
            # Handle structured content
            for part in message['content']:
                if 'text' in part : 
                    if isinstance(part.get('text', None), str):
                        # If the part has a text key, treat it as plain text
                        formatted_inputs.append(part['text'])  # type: ignore
                if 'data' in part: 
                    if isinstance(part.get('data', None), bytes):
                        # Handle binary data
                        formatted_inputs.append({ # type: ignore
                            "mime_type": part.get("mime_type", "application/octet-stream"), # type: ignore
                            "data": base64.b64encode(part["data"]).decode('utf-8') # type: ignore
                        }) # type: ignore
                elif 'data' in part: 
                    if isinstance(part.get('data', None), str):
                        # Handle string data with a mime_type
                        formatted_inputs.append({ # type: ignore
                            "mime_type": part.get("mime_type", "text/plain"), # type: ignore
                            "data": part["data"] # type: ignore
                        }) # type: ignore
                if part.get('type') == 'image_url':
                    if 'image_url' in part:
                        # Handle image URLs containing base64-encoded data
                        url = part['image_url'].get('url', '')  # type: ignore
                        if url.startswith('data:image/jpeg;base64,'):
                            # Extract base64 data and add it to the formatted inputs
                            base64_data = url.replace('data:image/jpeg;base64,', '')
                            formatted_inputs.append({ # type: ignore
                                "mime_type": "image/jpeg",
                                "data": base64_data # type: ignore
                            }) # type: ignore   
    
    return formatted_inputs
    
def convert_to_anthropic_format(
    messages: List[ChatCompletionUiformMessage]
) -> tuple[str, List[MessageParam]]:
    """
    Converts a list of ChatCompletionUiformMessage to a format compatible with the Anthropic SDK.

    Args:
        messages (List[ChatCompletionUiformMessage]): List of chat messages.

    Returns:
        (system_message, formatted_messages):
            system_message (str | NotGiven):
                The system message if one was found, otherwise NOT_GIVEN.
            formatted_messages (List[MessageParam]):
                A list of formatted messages ready for Anthropic.
    """

    formatted_messages: list[MessageParam] = []
    system_message: str = ""

    for message in messages:
        content_blocks: list[Union[TextBlockParam, ImageBlockParam]] = []

        # -----------------------
        # Handle system message
        # -----------------------
        if message["role"] == "system":
            assert isinstance(message["content"], str), "System message content must be a string."
            if system_message != "":
                raise ValueError("Only one system message is allowed per chat.")
            system_message+= message["content"]
            continue

        # -----------------------
        # Handle non-system roles
        # -----------------------
        if isinstance(message['content'], str):
            # Direct string content is treated as a single text block
            content_blocks.append({
                "type": "text",
                "text": message['content'],
            })

        elif isinstance(message['content'], list):
            # Handle structured content
            for part in message['content']:
                if part["type"] == "text":
                    part = cast(ChatCompletionContentPartTextParam, part)
                    content_blocks.append({
                        "type": "text",
                        "text": part['text'],  # type: ignore
                    })

                elif part["type"] == "input_audio":
                    part = cast(ChatCompletionContentPartInputAudioParam, part)
                    logging.warning("Audio input is not supported yet.")
                    # No blocks appended since not supported

                elif part["type"] == "image_url":
                    # Handle images that may be either base64 data-URLs or standard remote URLs
                    part = cast(ChatCompletionContentPartImageParam, part)
                    image_url = part["image_url"]["url"]

                    if "base64," in image_url:
                        # The string is already something like: data:image/jpeg;base64,xxxxxxxx...
                        media_type, data_content = image_url.split(";base64,")
                        # media_type might look like: "data:image/jpeg"
                        media_type = media_type.split("data:")[-1]  # => "image/jpeg"
                        base64_data = data_content
                    else:
                        # It's a remote URL, so fetch, encode, and derive media type from headers
                        try:
                            r = requests.get(image_url)
                            r.raise_for_status()
                            content_type = r.headers.get("Content-Type", "image/jpeg")
                            # fallback "image/jpeg" if no Content-Type given

                            # Only keep recognized image/* for anthropic
                            if content_type not in (
                                "image/jpeg", "image/png", "image/gif", "image/webp"
                            ):
                                logging.warning(
                                    "Unrecognized Content-Type '%s' - defaulting to image/jpeg",
                                    content_type,
                                )
                                content_type = "image/jpeg"

                            media_type = content_type
                            base64_data = base64.b64encode(r.content).decode("utf-8")

                        except Exception:
                            logging.warning(
                                "Failed to load image from URL: %s",
                                image_url,
                                exc_info=True,
                                stack_info=True,
                            )
                            # Skip adding this block if error
                            continue

                    # Finally, append to content blocks
                    content_blocks.append({
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": cast(MediaType, media_type),
                            "data": base64_data,
                        }
                    })

        formatted_messages.append(MessageParam(
            role=message["role"],  # type: ignore
            content=content_blocks
        ))

    return system_message, formatted_messages

def convert_to_openai_format(messages: List[ChatCompletionUiformMessage]) -> List[ChatCompletionMessageParam]:
    return cast(list[ChatCompletionMessageParam], messages)
    

def str_messages(messages: list[ChatCompletionUiformMessage], max_length: int = 100) -> str:
    """
    Converts a list of chat messages into a string representation with faithfully serialized structure.

    Args:
        messages (list[ChatCompletionUiformMessage]): The list of chat messages.
        max_length (int): Maximum length for content before truncation.

    Returns:
        str: A string representation of the messages with applied truncation.
    """
    def truncate(text: str, max_len: int) -> str:
        """Truncate text to max_len with ellipsis."""
        return text if len(text) <= max_len else f"{text[:max_len]}..."

    serialized: list[ChatCompletionUiformMessage] = []
    for message in messages:
        role = message["role"]
        content = message["content"]

        if isinstance(content, str):
            serialized.append({"role": role, "content": truncate(content, max_length)})
        elif isinstance(content, list):
            truncated_content: list[ChatCompletionContentPartParam] = []
            for part in content:
                if part["type"] == "text" and part["text"]:
                    truncated_content.append({"type": "text", "text": truncate(part["text"], max_length)})
                elif part["type"] == "image_url" and part["image_url"]:
                    image_url = part["image_url"].get("url", "unknown image")
                    truncated_content.append({"type": "image_url", "image_url": {"url": truncate(image_url, max_length)}})
            serialized.append({"role": role, "content": truncated_content})

    return repr(serialized)


class DocumentProcessingConfig(BaseModel):
    modality: Modality
    """The modality of the document to load."""

    image_settings : ImageSettings = Field(default_factory=ImageSettings, description="Preprocessing operations applied to image before sending them to the llm")
    """The image operations to apply to the document."""

from typing import Dict

class MessageConfig(DocumentProcessingConfig):
    json_schema: Dict = Field(..., description="JSON schema to validate the email data")

class ExtractionConfig(BaseModel):
    model: str = "gpt-4o-mini"
    temperature: float = 0
    

class DocumentCreateMessageRequest(DocumentProcessingConfig):
    document: MIMEData
    """The document to load."""




class DocumentMessage(BaseModel):
    id: str
    """A unique identifier for the document loading."""

    object: Literal["document_message"] = Field(default="document_message")
    """The type of object being loaded."""

    messages: List[ChatCompletionUiformMessage] 
    """A list of messages containing the document content and metadata."""

    created: int
    """The Unix timestamp (in seconds) of when the document was loaded."""

    modality: Modality
    """The modality of the document to load."""
    
    @property
    def items(self) -> list[str | PIL.Image.Image]:
        """Returns the document contents as a list of strings and images.

        This property processes the message content and converts it into a list of either
        text strings or PIL Image objects. It handles various content types including:
        - Plain text
        - Base64 encoded images
        - Remote image URLs
        - Audio data (represented as truncated string)

        Returns:
            list[str | PIL.Image.Image]: A list containing either strings for text content
                or PIL.Image.Image objects for image content. Failed image loads will
                return their URLs as strings instead.
        """
        results: list[str | PIL.Image.Image] = []
        
        for msg in self.messages:
            if isinstance(msg["content"], str):
                results.append(msg["content"])
                continue
            assert isinstance(msg["content"], list), "content must be a list or a string"
            for content_item in msg["content"]:
                if isinstance(content_item, str):
                    results.append(content_item)
                else:
                    item_type = content_item.get("type")
                    # If item is an image
                    if item_type == "image_url":
                        assert "image_url" in content_item, "image_url is required in ChatCompletionContentPartImageParam"
                        image_data_url = content_item["image_url"]["url"] # type: ignore

                        # 1) Base64 inline data
                        if image_data_url.startswith("data:image/"):
                            try:
                                prefix, base64_part = image_data_url.split(",", 1)
                                img_bytes = base64.b64decode(base64_part)
                                img = PIL.Image.open(BytesIO(img_bytes))
                                results.append(img)
                            except Exception as e:
                                print(f"Error decoding base64 data:\n  {e}")
                                results.append(image_data_url)

                        # 2) Otherwise, assume it's a remote URL
                        else:
                            try:
                                response = requests.get(image_data_url)
                                response.raise_for_status()  # raises HTTPError if not 200
                                img = PIL.Image.open(BytesIO(response.content))
                                results.append(img)
                            except Exception as e:
                                # Here, log or print the actual error
                                print(f"Could not download image from {image_data_url}:\n  {e}")
                                results.append(image_data_url)

                    # If item is text (or other types)
                    elif item_type == "text":
                        text_value = content_item.get("text", "")
                        assert isinstance(text_value, str), "text is required in ChatCompletionContentPartTextParam"
                        results.append(text_value)

                    elif item_type == "input_audio":
                        # Handle audio input content
                        if "input_audio" in content_item:
                            audio_data = content_item["input_audio"]["data"] # type: ignore
                            results.append(f"Audio data: {audio_data[:100]}...")  # Truncate long audio data

                    else:
                        # Fallback for unrecognized item types
                        results.append(f"Unrecognized type: {item_type}")

        return results

    @property
    def openai_messages(self) -> list[ChatCompletionMessageParam]:
        """Returns the messages formatted for OpenAI's API.

        Converts the internal message format to OpenAI's expected format for
        chat completions.

        Returns:
            list[ChatCompletionMessageParam]: Messages formatted for OpenAI's chat completion API.
        """
        return convert_to_openai_format(self.messages)


    @property
    def anthropic_messages(self) -> list[MessageParam]:
        """Returns the messages formatted for Anthropic's Claude API.

        Converts the internal message format to Claude's expected format,
        handling text, images, and other content types appropriately.

        Returns:
            list[MessageParam]: Messages formatted for Claude's API.
        """
        return convert_to_anthropic_format(self.messages)[1]
    
    @property
    def gemini_messages(self) -> content_types.ContentsType:
        """Returns the messages formatted for Google's Gemini API.

        Converts the internal message format to Gemini's expected format,
        handling various content types including text and images.

        Returns:
            content_types.ContentsType: Messages formatted for Gemini's API.
        """
        return convert_to_google_genai_format(self.messages)

    
    def __str__(self)->str:
        return f"DocumentMessage(id={self.id}, object={self.object}, created={self.created}, messages={str_messages(self.messages)}, modality={self.modality})"
    
    def __repr__(self)->str:
        return f"DocumentMessage(id={self.id}, object={self.object}, created={self.created}, messages={str_messages(self.messages)}, modality={self.modality})"
    